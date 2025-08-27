#include <iostream>
#include <sstream>
#include <chrono>
#include <thread>
#include <iomanip>
#include "driver/i2c_master.h"
#include "I2CSetup.h"
#include "ble_server.h"

extern "C" [[noreturn]] void app_main(void) {
    init_bluetooth();
    std::ostringstream oss;
    uint8_t data[2]{};
    i2c_master_bus_handle_t bus_handle;
    i2c_master_dev_handle_t mpu_handle, hmc_handle, bmp_handle;

    i2c_master_init(&bus_handle, &mpu_handle, &hmc_handle, &bmp_handle);

    std::cout << "[Info] Detecting sensors..." << std::endl;
    mpu6050_register_read(mpu_handle, MPU6050_WHO_AM_I_REG, data, 1);
    if (data[0] == 0) {oss << "[Error] Cannot find MPU6050!\n";} else {data[0] = 0; oss << "[Info] MPU6050 found!\n";}
    
    std::cout << "[Info] Waking up MPU6050..." << std::endl;
    mpu6050_register_write_byte(mpu_handle, MPU6050_PWR_MGMT_1, 0x00);
    
    hmc5883l_register_read(hmc_handle, HMC5883L_ADDR, data, 1);
    if (data[0] == 0) {oss << "[Error] Cannot find HMC5883L!\n";} else {data[0] = 0; oss << "[Info] HMC5883L found!\n";}
    bmp180_register_read(bmp_handle, BMP180_ACCESS, data, 1);
    if (data[0] == 0) {oss << "[Error] Cannot find BMP180!\n";} else {data[0] = 0; oss << "[Info] BMP180 found!\n";}
    std::cout << oss.str() << std::endl;

    int16_t mpu6050_sensor_data[7];
    uint8_t raw_data[14];
    float mpu6050_data_handler[7];
    while (true) {
        std::cout << "[Info] Still Alive "<< std::endl;
        // 7 registers store data in continuous memory each has 2 bytes int
        mpu6050_register_read(mpu_handle, MPU6050_ACCEL_XOUT_H, raw_data, 14);
        for (int i = 0; i < 7; i++) {
            // Convert raw bytes to signed 16-bit values
            mpu6050_sensor_data[i] = static_cast<int16_t>(raw_data[i * 2] << 8 | raw_data[i * 2 + 1]);
            
            // Convert to proper units
            if (i <= 2) { // Accelerometer: convert to g-force
                mpu6050_data_handler[i] = static_cast<float>(mpu6050_sensor_data[i]) / 16384.0f;
            } else if (i == 3) { // Temperature: convert to °C
                mpu6050_data_handler[i] = static_cast<float>(mpu6050_sensor_data[i]) / 340.0f + 36.53f;
            } else {
                constexpr float gyro_offset[3] = {-6.9, 0.3, 0.4}; // calibrated to closer to 0 when stationary
                // Gyroscope: convert to °/s
                mpu6050_data_handler[i] = static_cast<float>(mpu6050_sensor_data[i]) / 131.0f - gyro_offset[i-4];
            }
        }
        std::cout << std::fixed << std::setprecision(3);
        // std::cout << "MPU6050 | Accel(g): X=" << std::setw(7) << mpu6050_data_handler[0] 
        //           << " Y=" << std::setw(7) << mpu6050_data_handler[1]
        //           << " Z=" << std::setw(7) << mpu6050_data_handler[2]
        //           << " | Temp: " << std::setw(6) << mpu6050_data_handler[3] << "°C"
        //           << " | Gyro(°/s): X=" << std::setw(8) << mpu6050_data_handler[4]
        //           << " Y=" << std::setw(8) << mpu6050_data_handler[5] 
        //           << " Z=" << std::setw(8) << mpu6050_data_handler[6] << std::endl;
        
        oss.clear(); 
        oss << "MPU6050 | Accel(g): X=" << std::setw(7) << mpu6050_data_handler[0] 
                  << " Y=" << std::setw(7) << mpu6050_data_handler[1]
                  << " Z=" << std::setw(7) << mpu6050_data_handler[2]
                  << " | Temp: " << std::setw(6) << mpu6050_data_handler[3] << "°C"
                  << " | Gyro(°/s): X=" << std::setw(8) << mpu6050_data_handler[4]
                  << " Y=" << std::setw(8) << mpu6050_data_handler[5] 
                  << " Z=" << std::setw(8) << mpu6050_data_handler[6] << std::endl;

        send_message_to_client(oss.str().c_str());
        std::cout << "Message sent via BLE." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}