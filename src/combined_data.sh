 awk 'FNR==1 && NR!=1{next;}{print}' ../data/*/merged_health_data.csv > ../data/combined_health_data.csv

