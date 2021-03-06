until wpa_cli -i wlan0 reconfigure; do
  echo "Failed to reconfigure wlan0 with wpa_cli."
  echo "Restarting dhcpcd with systemctl."
  sudo systemctl daemon-reload
  sudo systemctl restart dhcpcd
  sudo ifconfig wlan0 up
  sleep 5
done
