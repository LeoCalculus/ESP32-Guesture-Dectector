#include <iostream>
#include <sstream>
#include <chrono>
#include <thread>
#include <iomanip>
#include <cstdlib>
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
    int counter_print_times = 0;
    int print_flag = 0;
    int case_number = 0;
    while (true) {
        mpu6050_register_read(mpu_handle, MPU6050_ACCEL_XOUT_H, raw_data, 14);
        for (int i = 0; i < 7; i++) {
            mpu6050_sensor_data[i] = static_cast<int16_t>(raw_data[i * 2] << 8 | raw_data[i * 2 + 1]);
            
            if (i <= 2) { // should have unit g
                mpu6050_data_handler[i] = static_cast<float>(mpu6050_sensor_data[i]) / 16384.0f;
            } else if (i == 3) { // Temperature °C
                mpu6050_data_handler[i] = static_cast<float>(mpu6050_sensor_data[i]) / 340.0f + 36.53f;
            } else {
                constexpr float gyro_offset[3] = {-6.9, 0.3, 0.4}; // calibrated to closer to 0 when stationary
                // Gyroscope °/s
                mpu6050_data_handler[i] = static_cast<float>(mpu6050_sensor_data[i]) / 131.0f - gyro_offset[i-4];
            }
        }

        if (abs(mpu6050_data_handler[4]) > 150 || abs(mpu6050_data_handler[5]) > 150 || abs(mpu6050_data_handler[6]) > 150){
            print_flag = 1;
            case_number++;
        }

        // a trigger for record
        if (print_flag == 1) { 
            counter_print_times++;
            oss.str(""); // clear string, or acculate data leads to memory corruption
            oss.clear();  // this only removes error flags not the content
            oss << std::fixed << std::setprecision(3) << mpu6050_data_handler[0] // X
                << " " << mpu6050_data_handler[1] // Y
                << " " << mpu6050_data_handler[2] // Z
                << " " << mpu6050_data_handler[4] // Gx
                << " " << mpu6050_data_handler[5] // Gy
                << " " << mpu6050_data_handler[6];// Gz
            send_message_to_client(oss.str().c_str());
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            counter_print_times++;
            if (counter_print_times >= 100) {
                counter_print_times = 0;
                print_flag = 0;
                send_message_to_client("Next");
            }
        }
    }
}