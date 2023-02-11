#include "freertos/FreeRTOS.h"
#include "esp_wifi.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "soc/rtc_wdt.h"
#include <stdio.h>
#include <stdint.h>

// Integer value 10 and 13, when converted to bytes from python side, one is b'\r' and the other is b'\n'
// and strangely enough, if we write it to the serial, the esp32 side will read both to be 10
// Something must be wrong with this serial write, but I don't have time to investigate into it
// I simply offset it
#define OFFSET 50
void send(const uint8_t *buf, uint32_t len) {
    for (int i=0; i<len; i++) {
        printf("%02x", buf[i]);
    }
}

void send_int(uint32_t i) {
    send((uint8_t*)&i, 4);
}

void send_packet(uint32_t ts_sec, uint32_t ts_usec, uint32_t len, const uint8_t* buf) {
    uint32_t incl_len = len > 2000 ? 2000 : len;

    printf("Packet % 3d.%06d %d %d\n", ts_sec, ts_usec, incl_len, len);

    printf("DATA:");
    send_int(ts_sec);
    send_int(ts_usec);
    send_int(incl_len);
    send_int(len);
    send(buf, incl_len);
    printf("\n");
}

void sniffer_callback(void *buf, wifi_promiscuous_pkt_type_t type){
    const wifi_promiscuous_pkt_t* pkt = (wifi_promiscuous_pkt_t*)buf;
    const wifi_pkt_rx_ctrl_t ctrl = (wifi_pkt_rx_ctrl_t)pkt->rx_ctrl;

    int64_t t = esp_timer_get_time();
    send_packet(t/1000000, t%1000000, ctrl.sig_len-4, pkt->payload);
}

void app_main() {
    nvs_flash_init();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    ESP_ERROR_CHECK(esp_wifi_set_storage(WIFI_STORAGE_RAM));
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));
    ESP_ERROR_CHECK(esp_wifi_start());
    esp_wifi_set_promiscuous(true);
    // Our connectivity bootloader has a wdt set up, so we need to reset it, if we want to use this firmware together with our bootloader
    // Nothing bad too
    rtc_wdt_feed();
    while (true)
    {
        int c = fgetc(stdin);
        c -= OFFSET;
        if(c >= 1 && c <= 14)
        {
            printf("Channel set to %d\n", c);
            esp_wifi_set_channel(c, WIFI_SECOND_CHAN_NONE);
            esp_wifi_set_promiscuous_rx_cb(sniffer_callback);
        }
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}
