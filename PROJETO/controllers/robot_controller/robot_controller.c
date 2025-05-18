#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <webots/robot.h>
#include <webots/motor.h>
#include <webots/distance_sensor.h>
#include <webots/led.h>
#include <webots/supervisor.h>

#define PASSO_TEMPO 32
#define QUANTIDADE_SENSORES_PROXIMIDADE 8
#define QUANTIDADE_LEDS 10
#define TAMANHO_MENSAGEM 256
#define VELOCIDADE_MAXIMA 6.28
#define LIMIAR_DISTANCIA 0.1
#define LIMIAR_OBSTACULO 80 
#define TEMPO_GIRO_90 500 
#define TEMPO_GIRO_45 250 
#define TEMPO_RECUO 200 
#define MAXIMO_GIROS_CONSECUTIVOS 5

typedef enum {
  MOVER_FRENTE,
  RECUAR,
  GIRAR_DIREITA_90,
  GIRAR_ESQUERDA_90,
  GIRAR_DIREITA_45,
  GIRAR_ESQUERDA_45,
  GIRAR_NO_LUGAR
} Estado;

int main(int argc, char **argv) {
  int i = 0;
  char Mensagem[TAMANHO_MENSAGEM] = {0};
  double LeiturasSensoresProximidade[QUANTIDADE_SENSORES_PROXIMIDADE];
  double AceleradorEsquerda = 1.0, AceleradorDireita = 1.0;
  Estado estado = MOVER_FRENTE;
  int passosGiro = 0;
  int caixaEncontrada = 0;
  int girosConsecutivos = 0;

  srand(time(NULL));

  wb_robot_init();

  WbNodeRef caixaLeve = wb_supervisor_node_get_from_def("CAIXA11");
  if (caixaLeve == NULL) {
    printf("Erro: CAIXA11 não encontrada! Verifique o arquivo .wbt.\n");
    wb_robot_cleanup();
    return 1;
  }

  WbDeviceTag MotorEsquerda = wb_robot_get_device("left wheel motor");
  WbDeviceTag MotorDireita = wb_robot_get_device("right wheel motor");
  wb_motor_set_position(MotorEsquerda, INFINITY);
  wb_motor_set_position(MotorDireita, INFINITY);
  wb_motor_set_velocity(MotorEsquerda, 0);
  wb_motor_set_velocity(MotorDireita, 0);

  WbDeviceTag SensoresProximidade[QUANTIDADE_SENSORES_PROXIMIDADE];
  char NomeSensor[10] = {0};
  for (i = 0; i < QUANTIDADE_SENSORES_PROXIMIDADE; i++) {
    sprintf(NomeSensor, "ps%d", i);
    SensoresProximidade[i] = wb_robot_get_device(NomeSensor);
    wb_distance_sensor_enable(SensoresProximidade[i], PASSO_TEMPO);
  }

  WbDeviceTag Leds[QUANTIDADE_LEDS];
  Leds[0] = wb_robot_get_device("led0");
  wb_led_set(Leds[0], -1);

  while (wb_robot_step(PASSO_TEMPO) != -1) {
    memset(Mensagem, 0, TAMANHO_MENSAGEM);

    for (i = 0; i < QUANTIDADE_SENSORES_PROXIMIDADE; i++) {
      LeiturasSensoresProximidade[i] = wb_distance_sensor_get_value(SensoresProximidade[i]);
      sprintf(Mensagem, "%s|ps%d: %6.0f  ", Mensagem, i, LeiturasSensoresProximidade[i]);
    }

    const double *PosicaoCaixa = wb_supervisor_node_get_position(caixaLeve);
    sprintf(Mensagem, "%s|CAIXA11 em x=%5.2f, y=%5.2f, z=%5.2f", Mensagem, PosicaoCaixa[0], PosicaoCaixa[1], PosicaoCaixa[2]);

    WbNodeRef noRobo = wb_supervisor_node_get_self();
    const double *posicaoRobo = wb_supervisor_node_get_position(noRobo);
    sprintf(Mensagem, "%s|Robô em x=%5.2f, y=%5.2f", Mensagem, posicaoRobo[0], posicaoRobo[1]);

    double dx = PosicaoCaixa[0] - posicaoRobo[0];
    double dy = PosicaoCaixa[1] - posicaoRobo[1];
    double distancia = sqrt(dx * dx + dy * dy);
    sprintf(Mensagem, "%s|Distância: %5.2f", Mensagem, distancia);

    sprintf(Mensagem, "%s|Estado: %d", Mensagem, estado);

    printf("%s\n", Mensagem);

    wb_led_set(Leds[0], wb_led_get(Leds[0]) * -1);

    if (!caixaEncontrada && distancia < LIMIAR_DISTANCIA) {
      caixaEncontrada = 1;
      estado = GIRAR_NO_LUGAR;
      printf("Caixa leve (CAIXA11) encontrada! Girando no eixo.\n");
    }

    switch (estado) {
      case MOVER_FRENTE:
        AceleradorEsquerda = 1.0;
        AceleradorDireita = 1.0;
        if (LeiturasSensoresProximidade[0] > LIMIAR_OBSTACULO || LeiturasSensoresProximidade[7] > LIMIAR_OBSTACULO ||
            LeiturasSensoresProximidade[1] > LIMIAR_OBSTACULO || LeiturasSensoresProximidade[6] > LIMIAR_OBSTACULO) {
          estado = RECUAR;
          passosGiro = TEMPO_RECUO / PASSO_TEMPO;
          girosConsecutivos++;
        } else {
          girosConsecutivos = 0;
        }
        break;

      case RECUAR:
        AceleradorEsquerda = -1.0;
        AceleradorDireita = -1.0;
        passosGiro--;
        if (passosGiro <= 0) {
          int angulo = (rand() % 2) ? 45 : 90;
          int direcao = (rand() % 2) ? 1 : -1; // 1 para direita, -1 para esquerda
          if (angulo == 45 && direcao == 1) estado = GIRAR_DIREITA_45;
          else if (angulo == 45 && direcao == -1) estado = GIRAR_ESQUERDA_45;
          else if (angulo == 90 && direcao == 1) estado = GIRAR_DIREITA_90;
          else estado = GIRAR_ESQUERDA_90;
          passosGiro = (angulo == 45 ? TEMPO_GIRO_45 : TEMPO_GIRO_90) / PASSO_TEMPO;
          if (girosConsecutivos >= MAXIMO_GIROS_CONSECUTIVOS) {
            passosGiro *= 2; 
            girosConsecutivos = 0;
          }
        }
        break;

      case GIRAR_DIREITA_90:
      case GIRAR_DIREITA_45:
        AceleradorEsquerda = 1.0;
        AceleradorDireita = -1.0;
        passosGiro--;
        if (passosGiro <= 0) {
          estado = MOVER_FRENTE;
        }
        break;

      case GIRAR_ESQUERDA_90:
      case GIRAR_ESQUERDA_45:
        AceleradorEsquerda = -1.0;
        AceleradorDireita = 1.0;
        passosGiro--;
        if (passosGiro <= 0) {
          estado = MOVER_FRENTE;
        }
        break;

      case GIRAR_NO_LUGAR:
        AceleradorEsquerda = 1.0;
        AceleradorDireita = -1.0;
        break;
    }

    wb_motor_set_velocity(MotorEsquerda, VELOCIDADE_MAXIMA * AceleradorEsquerda);
    wb_motor_set_velocity(MotorDireita, VELOCIDADE_MAXIMA * AceleradorDireita);
  };

  wb_robot_cleanup();
  return 0;
}