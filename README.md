# CC7711 Lab1

## 1. Descrição das intenções

```json
{
  "intents": [
    {
      "tag": "saudacao",
      "patterns": [
        "Olá",
        "Opa",
        "Oi",
        "Tudo bem?",
        "Como vai?",
        "E aí?",
        "Bom dia",
        "Boa tarde",
        "Boa noite",
        "Oi, tudo bem?",
        "Como você está?",
        "Saudações"
      ],
      "responses": [
        "Oi!",
        "Olá!",
        "Olá, tudo bem?",
        "Oi, tudo bem por aqui!",
        "Saudações!"
      ]
    },
    {
      "tag": "despedida",
      "patterns": [
        "Valeu",
        "Tchau",
        "Obrigado",
        "Fui",
        "Beleza",
        "Até mais",
        "Até logo",
        "Adeus",
        "Tenha um bom dia",
        "Tenha uma boa tarde",
        "Tenha uma boa noite",
        "Até a próxima"
      ],
      "responses": [
        "Até breve!",
        "Falou!",
        "Até mais!",
        "Tchau!",
        "Até a próxima!",
        "Tenha um bom dia!"
      ]
    },
    {
      "tag": "data_prova",
      "patterns": [
        "Quando será a prova?",
        "A prova será em que dia?",
        "Vai ter exame?",
        "Qual a data da prova?",
        "Que dia é a prova?",
        "A prova é quando?",
        "Data do exame",
        "Quando acontece a prova?",
        "Que dia será o exame?",
        "Exame será quando?"
      ],
      "responses": [
        "A prova será no dia 26.",
        "O exame será realizado no dia 26.",
        "A data da prova é dia 26.",
        "Está agendada para o dia 26."
      ]
    },
    {
      "tag": "agradecimento",
      "patterns": [
        "Obrigado",
        "Muito obrigado",
        "Agradeço",
        "Grato",
        "Valeu",
        "Muito grato",
        "Obrigada",
        "Muito obrigada",
        "Agradecida",
        "Muito agradecida"
      ],
      "responses": [
        "De nada!",
        "Por nada!",
        "Disponha!",
        "Não há de quê!",
        "Imagina!"
      ]
    },
    {
      "tag": "ajuda",
      "patterns": [
        "Você pode me ajudar?",
        "Preciso de ajuda",
        "Me ajuda por favor",
        "Suporte, por favor",
        "Como posso resolver o meu problema?"
      ],
      "responses": [
        "Claro, estou aqui para ajudar!",
        "Em que posso ser útil?",
        "Conte comigo para resolver seu problema."
      ]
    },
    {
      "tag": "horario_atendimento",
      "patterns": [
        "Qual o horário de atendimento?",
        "Quando vocês atendem?",
        "Quais são os horários de atendimento?",
        "Atendimento em que dias?",
        "Horário de funcionamento"
      ],
      "responses": [
        "Nosso atendimento é de segunda a sexta, das 9h às 18h.",
        "Funcionamos de segunda a sexta, das 9h às 18h."
      ]
    },
    {
      "tag": "localizacao",
      "patterns": [
        "Onde vocês estão localizados?",
        "Qual o endereço?",
        "Local da empresa",
        "Onde fica a empresa?",
        "Me mostre o endereço"
      ],
      "responses": [
        "Estamos localizados na Avenida Paulista, 1000.",
        "Nosso endereço é Avenida Paulista, 1000."
      ]
    }
  ]
}
```

## 2. Figura com o Diálogo Proposto
![Imagem](https://github.com/YuriBykoff/CC7711/blob/main/figs/lab1-2section.png)

## 3. Link para um vídeo de até 2 minutos

[Video](https://www.youtube.com/watch?v=t2tQpW0s3oY)
