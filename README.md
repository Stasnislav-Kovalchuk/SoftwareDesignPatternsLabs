# SoftwareDesignPatternsLabs

python3 lab4/main.py --choose-output


docker exec -it lab4-my_kafka-1 sh -lc '/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic dental-clinic-csv-preview --from-beginning' --- для консолі з Виводом

cat > /tmp/lab4.kafka.json <<'JSON'
{
  "input": { "type": "file", "file": "dental_clinic/data/dental_data.csv", "max_rows": 20, "delimiter": ";" },
  "output": { "type": "kafka", "kafka": { "bootstrap_servers": "127.0.0.1:9092", "topic": "dental-clinic-csv-preview" } }
}
JSON
python3 lab4/main.py /tmp/lab4.kafka.json --- для надсилання

console: просто друк у stdout; найшвидше для демо/дебагу, але дані не зберігаються і їх складно “споживати” іншим сервісом.

file: запис у файл (json або jsonl); дані зберігаються локально, легко перевіряти/прикладати до звіту, але це не “стрім” і не для інтеграцій між сервісами.

kafka: відправка повідомлень у топік; це “черга/стрім” для інтеграцій (інші програми можуть читати), добре для асинхронної обробки і масштабування, але потрібен запущений брокер і consumer для перегляду.

redis: запис у Redis (у нас — list через RPUSH); швидко як тимчасове сховище/буфер/черга для простих сценаріїв, але це не повноцінний лог-стрім як Kafka і потребує Redis-сервера