/*
  Firmware Arduino para Telemetría y Control con Streamlit
  ========================================================
  Este sketch establece una comunicación serie bidireccional (9600 baudios)
  para ser controlado desde una interfaz gráfica desarrollada en Streamlit.

  Protocolo de Comunicación (Terminado en '\n'):
  -----------------------------------------------
  COMANDOS ENVIADOS DESDE STREAMLIT A ARDUINO:
    - "LED:1\n"    -> Enciende el LED conectado al pin 13.
    - "LED:0\n"    -> Apaga el LED del pin 13.
    - "PWM:<val>\n"-> Establece el ciclo de trabajo PWM en el pin 9 (0 a 255).
    - "READ\n"     -> Solicita una lectura inmediata de los sensores.

  RESPUESTAS ENVIADAS DESDE ARDUINO A STREAMLIT:
    - "ACK:LED:1\n" o "ACK:LED:0\n"
    - "ACK:PWM:<val>\n"
    - "DATA:POT=<val>,TEMP=<val>,LIGHT=<val>\n"
*/

const int PIN_LED = 13;       // LED integrado en la placa
const int PIN_PWM = 9;        // Salida analógica PWM (ej. control de brillo o motor)
const int PIN_POT = A0;       // Entrada analógica 0 (Potenciómetro)
const int PIN_LUZ = A1;       // Entrada analógica 1 (Fotocelda LDR)

unsigned long ultimoEnvio = 0;
const unsigned long INTERVALO_ENVIO_MS = 1000; // Envío periódico cada 1 segundo
int valorPWM = 0;
bool estadoLED = false;

void setup() {
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_PWM, OUTPUT);
  
  digitalWrite(PIN_LED, LOW);
  analogWrite(PIN_PWM, 0);

  // Inicializar comunicación serie a 9600 baudios
  Serial.begin(9600);
  while (!Serial) {
    ; // Esperar a que el puerto serie esté listo
  }
  
  // Mensaje de saludo / Handshake inicial
  Serial.println("ARDUINO_STREAMLIT_READY");
}

void loop() {
  // 1. Escuchar comandos entrantes desde Python / Streamlit
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim(); // Eliminar espacios o retornos de carro

    procesarComando(comando);
  }

  // 2. Envío periódico de telemetría a Streamlit
  unsigned long tiempoActual = millis();
  if (tiempoActual - ultimoEnvio >= INTERVALO_ENVIO_MS) {
    ultimoEnvio = tiempoActual;
    enviarTelemetria();
  }
}

void procesarComando(String cmd) {
  if (cmd == "LED:1") {
    estadoLED = true;
    digitalWrite(PIN_LED, HIGH);
    Serial.println("ACK:LED:1");
  } 
  else if (cmd == "LED:0") {
    estadoLED = false;
    digitalWrite(PIN_LED, LOW);
    Serial.println("ACK:LED:0");
  } 
  else if (cmd.startsWith("PWM:")) {
    String valStr = cmd.substring(4);
    int pwm = valStr.toInt();
    pwm = constrain(pwm, 0, 255);
    valorPWM = pwm;
    analogWrite(PIN_PWM, pwm);
    Serial.print("ACK:PWM:");
    Serial.println(pwm);
  } 
  else if (cmd == "READ") {
    enviarTelemetria();
  } 
  else {
    Serial.print("ERR:UNKNOWN_COMMAND:");
    Serial.println(cmd);
  }
}

void enviarTelemetria() {
  int rawPot = analogRead(PIN_POT);
  int rawLuz = analogRead(PIN_LUZ);
  
  // Simular cálculo de temperatura en °C a partir de valor analógico
  // (Ejemplo: sensor LM35 o fórmula de divisor resistivo)
  float temperatura = 20.0 + (rawPot / 1023.0) * 15.0;

  // Formato clave-valor separado por comas
  Serial.print("DATA:POT=");
  Serial.print(rawPot);
  Serial.print(",TEMP=");
  Serial.print(temperatura, 1);
  Serial.print(",LIGHT=");
  Serial.print(rawLuz);
  Serial.print(",LED=");
  Serial.print(estadoLED ? 1 : 0);
  Serial.print(",PWM=");
  Serial.println(valorPWM);
}
