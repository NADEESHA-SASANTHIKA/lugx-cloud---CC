#!/bin/bash
# Check and start port-forwards if not running
for svc in "svc/clickhouse 9000:9000" "svc/game-service 5000:5000" "svc/order-service 5001:5001"; do
    if ! pgrep -f "kubectl port-forward $svc" > /dev/null; then
        nohup kubectl port-forward $svc >> /home/ec2-user/clickhouse_port_forward.log 2>&1 &
    fi
done

# Run the Python script
python3 /home/ec2-user/lugx-cloud-cw/export_events.py >> /home/ec2-user/data_transfer.log 2>&1
