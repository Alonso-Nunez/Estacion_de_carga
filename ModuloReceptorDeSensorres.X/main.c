/*
 * File:   Multimetro_PIC18F4550.c
 * Author: Ismael Cervantes de Anda
 * Programa para implementar las funciones de Voltmetro, Ampermetro y Termómetro acupando el ADC y envío de datos por medio de UART
 * Created on 16 de marzo de 2023, 04:49 PM
 */

// PIC18F4550 Configuration Bit Settings

// 'C' source line config statements

// CONFIG1L
#pragma config PLLDIV = 1       // PLL Prescaler Selection bits (No prescale (4 MHz oscillator input drives PLL directly))
#pragma config CPUDIV = OSC1_PLL2// System Clock Postscaler Selection bits ([Primary Oscillator Src: /1][96 MHz PLL Src: /2])
#pragma config USBDIV = 1       // USB Clock Selection bit (used in Full-Speed USB mode only; UCFG:FSEN = 1) (USB clock source comes directly from the primary oscillator block with no postscale)

// CONFIG1H
#pragma config FOSC = XT_XT     // Oscillator Selection bits (XT oscillator (XT))
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor Enable bit (Fail-Safe Clock Monitor disabled)
#pragma config IESO = OFF       // Internal/External Oscillator Switchover bit (Oscillator Switchover mode disabled)

// CONFIG2L
#pragma config PWRT = ON        // Power-up Timer Enable bit (PWRT enabled)
#pragma config BOR = ON         // Brown-out Reset Enable bits (Brown-out Reset enabled in hardware only (SBOREN is disabled))
#pragma config BORV = 3         // Brown-out Reset Voltage bits (Minimum setting 2.05V)
#pragma config VREGEN = OFF     // USB Voltage Regulator Enable bit (USB voltage regulator disabled)

// CONFIG2H
#pragma config WDT = OFF        // Watchdog Timer Enable bit (WDT disabled (control is placed on the SWDTEN bit))
#pragma config WDTPS = 32768    // Watchdog Timer Postscale Select bits (1:32768)

// CONFIG3H
#pragma config CCP2MX = ON      // CCP2 MUX bit (CCP2 input/output is multiplexed with RC1)
#pragma config PBADEN = ON      // PORTB A/D Enable bit (PORTB<4:0> pins are configured as analog input channels on Reset)
#pragma config LPT1OSC = OFF    // Low-Power Timer 1 Oscillator Enable bit (Timer1 configured for higher power operation)
#pragma config MCLRE = ON       // MCLR Pin Enable bit (MCLR pin enabled; RE3 input pin disabled)

// CONFIG4L
#pragma config STVREN = ON      // Stack Full/Underflow Reset Enable bit (Stack full/underflow will cause Reset)
#pragma config LVP = OFF        // Single-Supply ICSP Enable bit (Single-Supply ICSP disabled)
#pragma config ICPRT = OFF      // Dedicated In-Circuit Debug/Programming Port (ICPORT) Enable bit (ICPORT disabled)
#pragma config XINST = OFF      // Extended Instruction Set Enable bit (Instruction set extension and Indexed Addressing mode disabled (Legacy mode))

// CONFIG5L
#pragma config CP0 = ON         // Code Protection bit (Block 0 (000800-001FFFh) is code-protected)
#pragma config CP1 = ON         // Code Protection bit (Block 1 (002000-003FFFh) is code-protected)
#pragma config CP2 = ON         // Code Protection bit (Block 2 (004000-005FFFh) is code-protected)
#pragma config CP3 = ON         // Code Protection bit (Block 3 (006000-007FFFh) is code-protected)

// CONFIG5H
#pragma config CPB = OFF        // Boot Block Code Protection bit (Boot block (000000-0007FFh) is not code-protected)
#pragma config CPD = OFF        // Data EEPROM Code Protection bit (Data EEPROM is not code-protected)

// CONFIG6L
#pragma config WRT0 = OFF       // Write Protection bit (Block 0 (000800-001FFFh) is not write-protected)
#pragma config WRT1 = OFF       // Write Protection bit (Block 1 (002000-003FFFh) is not write-protected)
#pragma config WRT2 = OFF       // Write Protection bit (Block 2 (004000-005FFFh) is not write-protected)
#pragma config WRT3 = OFF       // Write Protection bit (Block 3 (006000-007FFFh) is not write-protected)

// CONFIG6H
#pragma config WRTC = OFF       // Configuration Register Write Protection bit (Configuration registers (300000-3000FFh) are not write-protected)
#pragma config WRTB = OFF       // Boot Block Write Protection bit (Boot block (000000-0007FFh) is not write-protected)
#pragma config WRTD = OFF       // Data EEPROM Write Protection bit (Data EEPROM is not write-protected)

// CONFIG7L
#pragma config EBTR0 = OFF      // Table Read Protection bit (Block 0 (000800-001FFFh) is not protected from table reads executed in other blocks)
#pragma config EBTR1 = OFF      // Table Read Protection bit (Block 1 (002000-003FFFh) is not protected from table reads executed in other blocks)
#pragma config EBTR2 = OFF      // Table Read Protection bit (Block 2 (004000-005FFFh) is not protected from table reads executed in other blocks)
#pragma config EBTR3 = OFF      // Table Read Protection bit (Block 3 (006000-007FFFh) is not protected from table reads executed in other blocks)

// CONFIG7H
#pragma config EBTRB = OFF      // Boot Block Table Read Protection bit (Boot block (000000-0007FFh) is not protected from table reads executed in other blocks)

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

#include <xc.h>
#include <stdio.h>
#include <pic18f4550.h>

#define _XTAL_FREQ 4000000

#define Led0 LATCbits.LATC0

#define Bit7_LCD LATDbits.LATD7
#define Bit6_LCD LATDbits.LATD6
#define Bit5_LCD LATDbits.LATD5
#define Bit4_LCD LATDbits.LATD4
#define Enable_LCD LATDbits.LATD3
#define RS_LCD LATDbits.LATD2

#define RxUART PORTCbits.RC7
#define TxUART LATCbits.LATC6

#define CHS3 ADCON0bits.CHS3
#define CHS2 ADCON0bits.CHS2
#define CHS1 ADCON0bits.CHS1
#define CHS0 ADCON0bits.CHS0
#define GO_DONE ADCON0bits.GO_DONE
#define ADON ADCON0bits.ADON

#define ADIE PIE1bits.ADIE
#define ADIF PIR1bits.ADIF

#define GIE INTCONbits.GIE_GIEH
#define TOIE INTCONbits.T0IE
#define TOIF INTCONbits.T0IF
#define PEIE INTCONbits.PEIE_GIEL

#define SPEN RCSTAbits.SPEN
#define CREN RCSTAbits.CREN

#define TRMT TXSTAbits.TRMT

#define RCIE PIE1bits.RCIE
#define TXIE PIE1bits.TXIE
#define RCIP IPR1bits.RCIP

#define TXIF PIR1bits.TXIF
#define RCIF PIR1bits.RCIF

#define EEPGD EECON1bits.EEPGD
#define WR EECON1bits.WR
#define WREN EECON1bits.WREN
#define RD EECON1bits.RD
#define EEIE PIE2bits.EEIE
#define EEIF PIR2bits.EEIF

#define IPEN RCONbits.IPEN

#define RBIF INTCONbits.RBIF
#define RBIE INTCONbits.RBIE

#define RBIP INTCON2bits.RBIP

char TxUSART;
char BufferLleno;
char BanderaRx;
char Num_Caracteres = 2;
char FinRx;
char ByteSup;
char ByteInf;
char BanderaADC;
char Instrumento = 0;
unsigned int ValBIN;
unsigned char var = '0';

char MensajeSobrante[] = "xx\n"; //3 Caracteres
char MensajeRx[] = "xx\n"; //3 Caracteres
char MensajeTx[5];

void Lcd_Port(char a) {
    if (a & 1)
        Bit4_LCD = 1;
    else
        Bit4_LCD = 0;

    if (a & 2)
        Bit5_LCD = 1;
    else
        Bit5_LCD = 0;

    if (a & 4)
        Bit6_LCD = 1;
    else
        Bit6_LCD = 0;

    if (a & 8)
        Bit7_LCD = 1;
    else
        Bit7_LCD = 0;
}

void Lcd_Cmd(char a) {
    RS_LCD = 0; // => RS = 0
    Lcd_Port(a);
    Enable_LCD = 1; // => E = 1
    __delay_ms(4);
    Enable_LCD = 0; // => E = 0
}

void lcd_clear() {
    Lcd_Cmd(0);
    Lcd_Cmd(1);
}

void lcd_gotoxy(char a, char b) {
    char temp, z, y;
    if (a == 1) {
        temp = 0x80 + b - 1;
        z = temp >> 4;
        y = temp & 0x0F;
        Lcd_Cmd(z);
        Lcd_Cmd(y);
    } else if (a == 2) {
        temp = 0xC0 + b - 1;
        z = temp >> 4;
        y = temp & 0x0F;
        Lcd_Cmd(z);
        Lcd_Cmd(y);
    }
}

void lcd_init() {
    Lcd_Port(0x00);
    __delay_ms(20);
    Lcd_Cmd(0x03);
    __delay_ms(5);
    Lcd_Cmd(0x03);
    __delay_ms(11);
    Lcd_Cmd(0x03);
    /////////////////////////////////////////////////////
    Lcd_Cmd(0x02);
    Lcd_Cmd(0x02);
    Lcd_Cmd(0x08);
    Lcd_Cmd(0x00);
    Lcd_Cmd(0x0C);
    Lcd_Cmd(0x00);
    Lcd_Cmd(0x06);
}

void lcd_write_char(char a) {
    char temp, y;
    temp = a & 0x0F;
    y = a & 0xF0;
    RS_LCD = 1; // => RS = 1
    Lcd_Port(y >> 4); //Data transfer
    Enable_LCD = 1;
    __delay_us(40);
    Enable_LCD = 0;
    Lcd_Port(temp);
    Enable_LCD = 1;
    __delay_us(40);
    Enable_LCD = 0;
}

void lcd_putc(char *a) {
    int i;
    for (i = 0; a[i] != '\0'; i++)
        lcd_write_char(a[i]);
}

void lcd_shift_right() {
    Lcd_Cmd(0x01);
    Lcd_Cmd(0x0C);
}

void lcd_shift_left() {
    Lcd_Cmd(0x01);
    Lcd_Cmd(0x08);
}

void __interrupt(high_priority) VectorInterrupcion(void) {
    if (EEIF == 1) {
        EEIF = 0;
    } //interrupción por fin de escritura en EEPROM
    if (RCIF == 1) { //Interrupción por uso de USART (RS-232)
        GIE = 0; //Desactivación general de interrupciones
        if (BufferLleno == 0) {
            MensajeRx[BanderaRx] = RCREG;
            BanderaRx++;
            if (BanderaRx == Num_Caracteres) {
                BanderaRx = 0; //Recepciona la cantidad de Bytes que se indica en el registro "Num_Caracteres"
                FinRx = 1;
                BufferLleno = 1;
            }
        } else {
            MensajeSobrante[BanderaRx] = RCREG;
            BanderaRx++;
            if (BanderaRx == Num_Caracteres) {
                BanderaRx = 0;
            }
        } //Esta línea no permite que se desborde el mensaje recibido
        
        RCIF = 0; //Limpia la bandera de interrupción por recepción
        GIE = 1; //Activa las interrupciones
    }
    if (ADIF == 1) { //Interrupción por ADC
        GIE = 0;

        ByteSup = ADRESH;
        ByteInf = ADRESL;
        ValBIN = ADRESH;
        ValBIN = ValBIN << 8;
        ValBIN = ValBIN + ADRESL;
        BanderaADC = 1;

        GIE = 1; //Activación general de interrupciones
        ADIF = 0;
    }
}

void ConfigPIC(void) {
    TRISA = 0B00111111; //Puerto A como entradas
    TRISB = 0x00; //Puerto B como salidas
    TRISC = 0B10000000; //Puerto C bit 7 entrada, demás terminales como salidas
    TRISD = 0X00; //Puerto D como salidas
    TRISE = 0XFF; //Puerto E como entradas
    IPEN = 1; //Activa los niveles de prioridad en las interrupciones
    ADCON1 = 0x0F; //Configurar terminales de ingreso al ADC como e/s digitales
    CMCON = 0x07; //Configurar bits del puerto A como e/s digitales
    PORTD = 0;
}

void ConfigADC(void) {
    ADCON0 = 0B00000001; //Activa el módulo ADC
    ADCON1 = 0B00000000; //Configurar todas las terminales de acceso al ADC como analógicas
    ADCON2 = 0B10100001; //Justifica a la derecha, 8TDA, Fosc/8
    ADIE = 1; //Activación de interrupción por ADC
    ADIF = 0;
    GIE = 1; //Activación de interrpciones
    PEIE = 1; //Activación de interrupciones por periférico
}

void ConfigUSART(void) //Configuracion_USART  9600 BPS, sin bit de paridad, 1 bit stop
{
    TXSTA = 0B00100110;
    //TXEN = 1 //Habilitado el Transmisior
    //BRGH = 1 //Selección de alta velocidad
    //TRMT = 1 //Registro TXREG vacío
    RCSTA = 0B10010000;
    //Este bit es parte del registro RCSTA    SPEN =1;                    //Habilitacion del puerto de comunicacion serial
    //Este bit es parte del registro RCSTA    CREN = 1;                   //Activa la recepcion continua
    BAUDCON = 0B00000010;
    //WUE = 1 //Auto-Detección de la trama
    SPBRG = 25;
    TXIE = 0; //Desactiva interrupción por fin de transmición por usart.
    RCIP = 1; //Asigna alta prioridad a la interrupción por recepción por usart
    TXIF = 0;
    RCIF = 0;
    RCIE = 1; //Activar interrupción por fin de recepción por usart.
    GIE = 1; //Activar habilitador general de interrupciones.
    PEIE = 1; //Activar habilitador general de interrupciones por perifericos.
    RCREG = 0;
}

void Transmite(void) { //Transmite por RS-232 9600 BPS, sin bit de paridad, 1 bit stop
    TXREG = TxUSART;
    while (!TXIF);
    while (!TRMT); //Esta bandera es la que funciona para detectar cuando se vacia el buffer de transmisión
}

void Tx_USART(void) {
    TxUSART = ByteSup;
    Transmite();
    __delay_us(10);
    TxUSART = ByteInf;
    
    
    Transmite();
    __delay_us(10);
    lcd_clear();
    lcd_gotoxy(1, 1);
    lcd_putc(MensajeRx);
    lcd_putc(" INS=");
    lcd_write_char(Instrumento);
    lcd_gotoxy(2, 1);
    lcd_putc("VAL=");
    sprintf(MensajeTx, "%4i", ValBIN);
    lcd_putc(MensajeTx);
}

void main(void) {
    ConfigPIC();
    ConfigADC();
    ConfigUSART();
    lcd_init();
    
    Led0 = 0;
    
    while (1) {
        BanderaRx = 0;
        FinRx = 0;
        BufferLleno = 0;

        while (FinRx == 0); //Espera petición a través del Serial, aquí se queda hasta recibir 2 bytes

        if (FinRx == 1) {
            FinRx = 0;
            if (MensajeRx[0] == 'V') {
                Instrumento = 'V';
                CHS3 = 0;
                switch (MensajeRx[1]) {
                    case '1':
                        CHS0 = 0;
                        CHS1 = 0;
                        CHS2 = 0;
                        break;
                    case '2':
                        CHS0 = 1;
                        CHS1 = 0;
                        CHS2 = 0;
                        break;
                    case '3':
                        CHS0 = 0;
                        CHS1 = 1;
                        CHS2 = 0;
                        break;
                    case '4':
                        CHS0 = 1;
                        CHS1 = 1;
                        CHS2 = 0;
                        break;
                    case '5':
                        CHS0 = 0;
                        CHS1 = 0;
                        CHS2 = 1;
                        break;
                    default:
                        Instrumento = 0;
                }
            } else if (MensajeRx[0] == 'A') {
                Instrumento = 'A';
                CHS2 = 1;
                CHS3 = 0;
                switch (MensajeRx[1]) {
                    case '1':
                        CHS0 = 1;
                        CHS1 = 0;
                        break;
                    case '2':
                        CHS0 = 0;
                        CHS1 = 1;
                        break;
                    case '3':
                        CHS0 = 1;
                        CHS1 = 1;
                        break;
                    default:
                        Instrumento = 0;
                }
            } else if (MensajeRx[0] == 'T' && MensajeRx[1] == 'M') {
                Instrumento = 'T';
                CHS0 = 0;
                CHS1 = 0;
                CHS2 = 0;
                CHS3 = 1;
            } else if (MensajeRx[0] == 'H' && MensajeRx[1] == 'I') {
                Instrumento = 'H';
            } else {
                Instrumento = 0;
            }
        }

        if (Instrumento != 0) {
            if (Instrumento == 'H') {
                ByteSup = 'O'; //Contesta al proceso de gestión de conexión con OK
                ByteInf = 'K';
                Tx_USART();
            }
            while (Instrumento != 'H') {
                BanderaRx = 0;
                FinRx = 0;
                BufferLleno = 0;
                while (FinRx == 0) {
                    GO_DONE = 1; //Iniciar la operación del ADC
                    while (BanderaADC == 0); //Espera que termine proceso de digitalización del ADC
                    Tx_USART();
                    BanderaADC = 0;
                    __delay_ms(1000);
                }
                if (FinRx == 1) {
                    FinRx = 0;
                    if ((MensajeRx[0] == 'F') && (MensajeRx[1] == 'P')) {
                        Instrumento = 'H';
                    }
                }
            }
        } else {
            ByteSup = 'E'; //Contesta que el comando que recibio es erroneo
            ByteInf = 'R';
            Tx_USART();
        }
    }

    return;
}
