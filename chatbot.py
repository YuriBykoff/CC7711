import numpy as np
import json
import pickle
import nltk
import random
import ssl

# --- SSL Handling (Good practice, keep this) ---
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# --- NLTK Downloads (Do this *once*, outside the class) ---
nltk.download('all')

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential, load_model  # Use tensorflow.keras
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

class ChatBot:
    def __init__(self, intents_file='intents.json'):
        self.intents_file = intents_file  # Store the filename
        self.words = []
        self.classes = []
        self.documents = []
        self.intents = []  # Initialize as empty list
        self.model = None  # Initialize as None
        self.ignore_words = ['?', '!']
        self.lemmatizer = WordNetLemmatizer()

        self._load_intents()  # Load intents during initialization

    def _load_intents(self):
        """Loads intents from the JSON file."""
        try:
            with open(self.intents_file, encoding="utf8") as file:
                self.intents = json.load(file)
        except FileNotFoundError:
            print(f"Error: Intents file '{self.intents_file}' not found.")
            # Handle the error appropriately.  Exit, or raise the exception.
            raise  # Re-raise the exception to stop execution

    def createModel(self):
        """Cria e treina o modelo do chatbot."""
        # Processamento inicial dos dados
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                # Tokenização das palavras
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                # Adiciona aos documentos
                self.documents.append((w, intent['tag']))
                # Adiciona às classes
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        # Lematização e preparação das palavras
        self.words = [self.lemmatizer.lemmatize(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

        # Criação dos dados de treinamento
        training = []
        output_empty = [0] * len(self.classes)

        for doc in self.documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = [self.lemmatizer.lemmatize(word.lower()) for word in pattern_words]
            
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training, dtype=object)

        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        # Criação do modelo
        self.model = Sequential()
        self.model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(len(train_y[0]), activation='softmax'))

        # Compilação do modelo
        sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        # Treinamento do modelo
        self.model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

        # Salvar o modelo
        self.model.save('chatbot_model.h5')
        
        # Salvar palavras e classes
        with open('words.pkl', 'wb') as f:
            pickle.dump(self.words, f)
        with open('classes.pkl', 'wb') as f:
            pickle.dump(self.classes, f)

    def train(self):
        """Prepares data and trains the model."""

        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                self.documents.append((w, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [self.lemmatizer.lemmatize(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

        print(len(self.documents), "documents")
        print(len(self.classes), "classes", self.classes)
        print(len(self.words), "unique lemmatized words", self.words)


        # --- Data Preparation (Corrected) ---
        training = []
        output_empty = [0] * len(self.classes)
        for doc in self.documents:
            bag = []
            pattern_words = [self.lemmatizer.lemmatize(word.lower()) for word in doc[0]]
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])

        random.shuffle(training)
        # Let NumPy infer the dtype, or use dtype=float if you know it's numerical
        training = np.array(training)  # Removed dtype=object
        train_x = list(training[:, 0])
        train_y = list(training[:, 1])
        print("Training data created")

        # --- Model Building (Corrected Imports) ---
        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        # --- Training ---
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)  #epochs to 200
        self.model = model
        print("Model trained")
        return hist #Return history for analysis


    def save_model(self, model_path='chatbot_model.h5', words_path='words.pkl', classes_path='classes.pkl'):
        """Saves the trained model, words, and classes."""
        self.model.save(model_path)
        with open(words_path, 'wb') as f:
            pickle.dump(self.words, f)
        with open(classes_path, 'wb') as f:
            pickle.dump(self.classes, f)
        print("Model saved")


    def load_model(self, model_path='chatbot_model.h5', words_path='words.pkl', classes_path='classes.pkl'):
        """Loads a pre-trained model, words, and classes."""
        try:
            self.model = load_model(model_path)
            with open(words_path, 'rb') as f:
                self.words = pickle.load(f)
            with open(classes_path, 'rb') as f:
                self.classes = pickle.load(f)
            self._load_intents() # Make sure intents are loaded
            print("Model loaded successfully.")
        except (FileNotFoundError, OSError) as e:
            print(f"Error loading model: {e}")
            # Consider raising the exception or handling it gracefully
            self.model = None # Set model to None, if it failed to load


    def clean_up_sentence(self, sentence):
        """Tokenizes and lemmatizes a sentence."""
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def bow(self, sentence, show_details=False):
        """Creates a bag-of-words representation of a sentence."""
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return np.array(bag)

    def predict_class(self, sentence):
        """Predicts the intent class for a given sentence."""
        if self.model is None:
            print("Error: Model not loaded.  Please train or load a model.")
            return []  # Return an empty list to indicate failure

        p = self.bow(sentence, show_details=False)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def getResponse(self, ints):
        """Gets a response based on the predicted intent."""
        if not ints:  # Check if the list is empty
            return "I'm sorry, I don't understand."
        tag = ints[0]['intent']
        for i in self.intents['intents']:
            if i['tag'] == tag:
                return random.choice(i['responses'])
        return "I'm sorry, I don't understand." # Default response

    def chatbot_response(self, msg):
        """Provides a complete chatbot response."""
        ints = self.predict_class(msg)
        res = self.getResponse(ints)
        return res, ints
