# Tutorial 08: Interconexión de Arduino con Streamlit mediante Puerto Serie (PySerial)

Este tutorial enseña cómo conectar microcontroladores físicos (**Arduino**, **ESP32**, **Raspberry Pi Pico**) a un panel web interactivo en **Streamlit** utilizando comunicación serie bidireccional sobre USB.

---

## 🎯 Objetivos de Aprendizaje
- Conectar hardware externo usando la biblioteca `pyserial`.
- **Resolver el problema crítico del ciclo de vida en Streamlit**: Evitar que el Arduino se reinicie en cada clic de la interfaz gracias a `@st.cache_resource`.
- Diseñar un protocolo de comunicación serie robusto basado en comandos ASCII terminados en salto de línea (`\n`).
- Controlar salidas digitales (LED ON/OFF) y analógicas (modulación PWM).
- Adquirir y graficar telemetría en tiempo real de canales analógicos (potenciómetro, temperatura, sensor de luz).
- Probar la aplicación con **Modo Simulación Integrado** si no dispones de un Arduino conectado físicamente.

---

## ⚠️ El Gran Desafío de Streamlit con el Puerto Serie

En un script común de Python, abres el puerto serie al inicio y ejecutas un bucle `while True`.  
Sin embargo, **en Streamlit, el script se re-ejecuta desde la línea 1 con cada clic o interacción del usuario**:

1. Si intentas hacer `ser = serial.Serial('COM3', 9600)` sin caché:
   - En cada clic en la interfaz, Python intentará abrir el puerto nuevamente.
   - El puerto arrojará un error `SerialException: Access is denied` (porque ya está abierto).
   - O peor aún: alternar la línea DTR reiniciará el bootloader del microcontrolador cada 2 segundos.
2. **La Solución**: Encapsular el objeto de conexión dentro de una función decorada con **`@st.cache_resource`**:
   ```python
   @st.cache_resource
   def get_serial_manager(port: str, baudrate: int, simulated: bool):
       return ArduinoSerialManager(port, baudrate, simulated)
   ```
   Esto asegura que la conexión se inicialice **una sola vez** y permanezca viva e inalterada en memoria durante toda la sesión web.

---

## 🔌 Esquema de Conexiones Recomendado (Arduino Uno)

| Componente | Pin en Arduino | Función |
| :--- | :--- | :--- |
| **LED Integrado** | Pin 13 | Salida digital controlada por comandos `LED:1` y `LED:0` |
| **LED Externo + Resistencia 220Ω** | Pin ~9 (PWM) | Salida con modulación de ancho de pulso `PWM:0` a `PWM:255` |
| **Potenciómetro (Pin Central)** | Pin A0 | Lectura analógica de 0 a 1023 (tensión de 0V a 5V) |
| **Fotocelda LDR / Sensor de Luz** | Pin A1 | Lectura analógica de intensidad lumínica ambiental |
| **GND y 5V** | Pines GND y 5V | Alimentación de sensores analógicos |

---

## 📜 Protocolo de Comunicación (Serial a 9600 Baudios)

Todos los mensajes terminan con un carácter de salto de línea `\n`:

### De Streamlit a Arduino (Comandos):
- `LED:1\n` ➔ Enciende el LED del pin 13.
- `LED:0\n` ➔ Apaga el LED del pin 13.
- `PWM:180\n` ➔ Asigna ciclo de trabajo PWM de 180 al pin 9.
- `READ\n` ➔ Solicita lectura inmediata de sensores.

### De Arduino a Streamlit (Respuestas):
- `ACK:LED:1\n` / `ACK:LED:0\n` ➔ Confirmación de actuador digital.
- `ACK:PWM:<valor>\n` ➔ Confirmación de actuador PWM.
- `DATA:POT=512,TEMP=24.5,LIGHT=620,LED=1,PWM=128\n` ➔ Paquete estructurado de telemetría.

---

## 🛠️ Cómo Cargar el Firmware en el Arduino

1. Abre el archivo [`arduino_code/arduino_firmware.ino`](file:///e:/PROJECTS/STREAMLIT_CODES/08_arduino_serial_hardware/arduino_code/arduino_firmware.ino) en el **Arduino IDE**.
2. Conecta tu placa Arduino al puerto USB de tu computadora.
3. En el menú **Herramientas > Placa**, selecciona tu modelo (ej. *Arduino Uno*).
4. En **Herramientas > Puerto**, selecciona el puerto detectado (ej. `COM3` en Windows o `/dev/ttyUSB0` en Linux/Mac).
5. Haz clic en el botón **Subir** (Upload / Flecha hacia la derecha).
6. Cierra el Monitor Serie de Arduino IDE antes de abrir Streamlit (para que el puerto no quede ocupado).

---

## 🚀 Cómo Ejecutar la Aplicación Streamlit

Desde la raíz del proyecto:

```bash
uv run streamlit run 08_arduino_serial_hardware/app.py
```

> **¿No tienes un Arduino a la mano ahora mismo?**  
> ¡No te preocupes! El panel detectará automáticamente si no hay puertos COM disponibles y activará el **Modo Simulación**. Puedes encender/apagar el LED virtual, deslizar el PWM y ver las gráficas de telemetría respondiendo a señales senoidales realistas generadas matemáticamente.
