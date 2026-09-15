 awk 'FNR==1 && NR!=1{next;}{print}' */merged_health_data.csv > combined_health_data.csv

