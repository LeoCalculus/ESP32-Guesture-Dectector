//
// Created by Xuleo on 8/21/2025.
//

#ifndef ESP32TEST_I2CREADWRITE_H
#define ESP32TEST_I2CREADWRITE_H
#include "driver/i2c_master.h"
#include "freertos/FreeRTOS.h"
#include "esp_log.h"
#include "Constants.h"

// initialize
static void i2c_master_init(i2c_master_bus_handle_t *bus_handle, i2c_master_dev_handle_t *mpu_handle,
                            i2c_master_dev_handle_t *hmc_handle, i2c_master_dev_handle_t *bmp_handle)
{
    constexpr i2c_master_bus_config_t bus_config = {
        .i2c_port = I2C_MASTER_NUM,
        .sda_io_num = static_cast<gpio_num_t>(I2C_MASTER_SDA_IO),
        .scl_io_num = static_cast<gpio_num_t>(I2C_MASTER_SCL_IO),
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags = {.enable_internal_pullup = true}
    };
    ESP_ERROR_CHECK(i2c_new_master_bus(&bus_config, bus_handle));

    constexpr i2c_device_config_t mpu_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = MPU6050_ACCESS_ADDR,
        .scl_speed_hz = I2C_MASTER_FREQ_HZ,
    };
    ESP_ERROR_CHECK(i2c_master_bus_add_device(*bus_handle, &mpu_config, mpu_handle));

    constexpr i2c_device_config_t hmc_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = HMC5883L_ADDR,
        .scl_speed_hz = I2C_MASTER_FREQ_HZ,
    };
    ESP_ERROR_CHECK(i2c_master_bus_add_device(*bus_handle, &hmc_config, hmc_handle));

    constexpr i2c_device_config_t bmp_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = BMP180_ADDR,
        .scl_speed_hz = I2C_MASTER_FREQ_HZ,
    };
    ESP_ERROR_CHECK(i2c_master_bus_add_device(*bus_handle, &bmp_config, bmp_handle));
}

// read
static esp_err_t mpu6050_register_read(i2c_master_dev_handle_t dev_handle, uint8_t reg_addr, uint8_t *data, size_t len)
{
    return i2c_master_transmit_receive(dev_handle, &reg_addr, 1, data, len, I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
}

// write
static esp_err_t mpu6050_register_write_byte(i2c_master_dev_handle_t dev_handle, uint8_t reg_addr, uint8_t data)
{
    uint8_t write_buf[2] = {reg_addr, data};
    return i2c_master_transmit(dev_handle, write_buf, sizeof(write_buf), I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
}

static esp_err_t hmc5883l_register_read(i2c_master_dev_handle_t dev_handle, uint8_t reg_addr, uint8_t *data, size_t len)
{
    return i2c_master_transmit_receive(dev_handle, &reg_addr, 1, data, len, I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
}

static esp_err_t hmc5883l_register_write_byte(i2c_master_dev_handle_t dev_handle, uint8_t reg_addr, uint8_t data)
{
    uint8_t write_buf[2] = {reg_addr, data};
    return i2c_master_transmit(dev_handle, write_buf, sizeof(write_buf), I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
}

static esp_err_t bmp180_register_read(i2c_master_dev_handle_t dev_handle, uint8_t reg_addr, uint8_t *data, size_t len)
{
    return i2c_master_transmit_receive(dev_handle, &reg_addr, 1, data, len, I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
}

static esp_err_t bmp180_register_write_byte(i2c_master_dev_handle_t dev_handle, uint8_t reg_addr, uint8_t data)
{
    uint8_t write_buf[2] = {reg_addr, data};
    return i2c_master_transmit(dev_handle, write_buf, sizeof(write_buf), I2C_MASTER_TIMEOUT_MS / portTICK_PERIOD_MS);
}

#endif //ESP32TEST_I2CREADWRITE_H