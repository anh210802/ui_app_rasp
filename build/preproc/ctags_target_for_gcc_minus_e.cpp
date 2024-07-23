# 1 "F:\\esp32\\KILL-LOVE\\KILL-LOVE.ino"
# 2 "F:\\esp32\\KILL-LOVE\\KILL-LOVE.ino" 2
# 3 "F:\\esp32\\KILL-LOVE\\KILL-LOVE.ino" 2




const char* ssid = "KILL-LOVE";
const char* password = "";
int channel = 3;
int ssid_hidden = 0;
int max_connection = 4;

uint8_t MAC_Address[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

void setup_wifi_access_point();
void scan_wifi_networks();
void monitor_wifi_networks();

void setup() {
    Serial.begin(115200);
    Serial2.begin(115200, SERIAL_8N1, 16, 17);
    setup_wifi_access_point();
    scan_wifi_networks();
}

void loop() {
   scan_wifi_networks();
   delay(10000);
}

void setup_wifi_access_point() {
    WiFi.mode(WIFI_MODE_AP);
    WiFi.softAP(ssid, password, channel, ssid_hidden, max_connection);
    Serial.println("Access Point started");
    Serial.print("IP Address: ");
    Serial.println(WiFi.softAPIP());
    WiFi.softAPmacAddress(MAC_Address);
    Serial.print("MAC Address: ");
    for (int i = 0; i < 6; ++i) {
        if (i > 0) Serial.print(":");
        Serial.print(MAC_Address[i], 16);
    }
    Serial.println();
}

void scan_wifi_networks() {
    int num_networks = WiFi.scanNetworks();
    if (num_networks == 0) {
        Serial2.println("No networks found");
        return;
    } else {
        Serial2.print(num_networks);
        Serial2.println(" networks found");
        Serial2.println("St | SSID                             | MAC               | RSSI | CH | Encryption");
        for (int i = 0; i < num_networks; i++) {
            Serial2.printf("%2d | %-32s | %17s | %4d | %2d | ",
                          i + 1,
                          WiFi.SSID(i).c_str(),
                          WiFi.BSSIDstr(i).c_str(),
                          WiFi.RSSI(i),
                          WiFi.channel(i));

            switch(WiFi.encryptionType(i)) {
                case WIFI_AUTH_OPEN:
                    Serial2.println("Open");
                    break;
                case WIFI_AUTH_WEP:
                    Serial2.println("WEP");
                    break;
                case WIFI_AUTH_WPA_PSK:
                    Serial2.println("WPA");
                    break;
                case WIFI_AUTH_WPA2_PSK:
                    Serial2.println("WPA2");
                    break;
                case WIFI_AUTH_WPA_WPA2_PSK:
                    Serial2.println("WPA+WPA2");
                    break;
                case WIFI_AUTH_WPA2_ENTERPRISE:
                    Serial2.println("WPA2-EAP");
                    break;
                case WIFI_AUTH_WPA3_PSK:
                    Serial2.println("WPA3");
                    break;
                case WIFI_AUTH_WPA2_WPA3_PSK:
                    Serial2.println("WPA2+WPA3");
                    break;
                case WIFI_AUTH_WAPI_PSK:
                    Serial2.println("WAPI");
                    break;
                default:
                    Serial2.println("Unknown");
                    break;
            }
            delay(20);
        }
    }
    Serial2.println("");
}

void monitor_wifi_networks() {

}
