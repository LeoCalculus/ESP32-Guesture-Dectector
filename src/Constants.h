//
// Created by Xuleo on 8/21/2025.
//

#ifndef ESP32TEST_CONSTANTS_H
#define ESP32TEST_CONSTANTS_H

// Configuration for I2C Master, source: https://github.com/espressif/esp-idf/blob/v5.5/examples/peripherals/i2c/i2c_basic/main/i2c_basic_example_main.c
#define I2C_MASTER_SCL_IO           22            /*!< GPIO number used for I2C master clock */
#define I2C_MASTER_SDA_IO           21           /*!< GPIO number used for I2C master data  */
#define I2C_MASTER_NUM              I2C_NUM_0    /*!< I2C port number for master dev */
#define I2C_MASTER_FREQ_HZ          400000       /*!< I2C master clock frequency */
#define I2C_MASTER_TX_BUF_DISABLE   0            /*!< I2C master doesn't need buffer */
#define I2C_MASTER_RX_BUF_DISABLE   0            /*!< I2C master doesn't need buffer */
#define I2C_MASTER_TIMEOUT_MS       1000

#define MPU6050_ACCESS_ADDR    0x68 // MPU6050 I2C address
#define MPU6050_WHO_AM_I_REG   0x75 // WHO_AM_I register address
#define MPU6050_PWR_MGMT_1     0x6B // Wake up sensor
#define MPU6050_ACCEL_XOUT_H   0x3B // Accelerometer X-axis high byte (start of data registers)

#define HMC5883L_ADDR          0x0D
#define HMC5883L_WRITE         0x3C
#define HMC5883L_READ          0x3D
#define HMC5883L_ID1           0x0A
#define HMC5883L_ID2           0x0B
#define HMC5883L_ID3           0x0C

#define BMP180_ADDR            0x77
#define BMP180_ACCESS          0xD0
#define BMP180_WRITE           0xEE
#define BMP180_READ            0xEF



#endif //ESP32TEST_CONSTANTS_H