# RAG Evaluation Results

| ID | Question | Expected | Top-1 score | Top-1 source | Boundary |
|---:|---|---|---:|---|---|
| 1 | What are major risk factors for heart disease? | answerable | 0.4386 | cdc_heart_disease_risk.md | no |

**Q1 answer mode:** llm-ollama-tinyllama
**Answer:** Major risk factors for heart disease include high blood pressure, high cholesterol, and smoking. Some risk factors cannot be controlled, such as age and family history, while other factors can be changed through healthier behavior and management of health conditions. High blood pressure, high cholesterol, and smoking are all modifiable risk factors that can be controlled through lifestyle changes and medication. Family history and age can also influence risk, but these factors can be managed through lifestyle changes and appropriate management. Modifiable risk factors include unhalelthy diets, excessive salt intake, physical inactivity, tobacco use, harmful alcohol use, and overweight or obe

| 2 | What lifestyle factors can increase the risk of high blood pressure? | answerable | 0.5278 | cdc_high_blood_pressure.md | no |

**Q2 answer mode:** llm-ollama-tinyllama
**Answer:** Lifestyle factors can increase the risk of high blood pressure, including physical inactivity, unhealthy diet, some medical conditions such as diabetes, too much alcohol and tobacco use. Family history and age can also influence risk. Health conditions, such as high blood pressure, can be controlled through healthier choices and appropriate management. Modifiable risk factors include unhappy diets, excessive salt intake, physical inactivity, tobacco use, harmful alcohol use, and overweight or obesity. Family history, older age, and conditions such as diabetes or kidney disease are non-modifiable or associated risk factors. Management includes reducing modifiable risk factors, checking blood 

| 3 | How much moderate-intensity activity is recommended for adults each week? | answerable | 0.4936 | who_physical_activity.md | no |

**Q3 answer mode:** llm-ollama-tinyllama
**Answer:** The available evidence suggests that adults should aim for at least 150 minutes of moderate-intensity aerobic physical activity per week, or 75 minutes of vigorous-intensity activity, or an equivalent combination, for a total of at least 300 minutes per week. This includes at least 21 days of moderate-intensity activity and 18 days of vigorous-intensity activity. Regular physical activity can provide important health benefits for chronic disease prevention, including lowering the risk of heart disease, stroke, and type 2 diabetes, improving sleep, and reducing the risk of weight gain. Hypertension is a persistently raised blood pressure that can increase the risk of heart, brain, kidney, and

| 4 | What are the core principles of a healthy diet? | answerable | 0.3331 | who_healthy_diet.md | no |

**Q4 answer mode:** llm-ollama-tinyllama
**Answer:** The core principles of a healthy diet are adequacy, balance, moderation, and variety. Dietary recommendations include minimizing processed and unprocessed foods, consuming a variety of whole grains, vegetables, fruits, pulse, and other nutritious foods, limiting salt intake, and aiming for at least 400 grams of fruit and vegetables per day. Physical activity provides important health benefits for chronic disease prevention, including lowering the risk of heart disease, stroke, and type 2 diabetes, improving sleep, and reducing short-term anxiety. Regular physical activity is relevant to blood pressure and overall cardiovascular health. Modifiable risk factors include unhämtliche diet, excess

| 5 | Why is blood pressure measurement important for hypertension? | answerable | 0.4144 | who_hypertension.md | no |

**Q5 answer mode:** llm-ollama-tinyllama
**Answer:** Blood pressure measurement is important for hypertension because it can increase the risk of heart, brain, kidney, and other diseasees. Many people do not notice symptoms, so measurement of blood pressure is important for detection. Modifiable risk factors include unhappy dieats, excessive salt intake, physical inactivity, tobacco use, and harmful alcohol use. Family history, older age, and conditions such as diabetes or kidney disease are non-modifiable or associated risk factors. Management includes reducing modifiable risk factors, checking blood pressure regularly, and consulting health professionals.

| 6 | How can physical activity affect cardiovascular health? | answerable | 0.5183 | cdc_physical_activity.md | no |

**Q6 answer mode:** llm-ollama-tinyllama
**Answer:** Physical activity can have a positive impact on cardiovascular health by improving sleep, reducing short-term anxiety, and lowering the risk of heart disease, stroke, and type 2 diabetes. Regular physical activity can also help reduce the risk of weight gain and improve blood pressure and overall cardiovascular health. The WHO recommends at least 150 minutes of moderate-intensity aerobic physical activity per week, or 75 minutes of vigorous-intensity activity, or an equivalent combination, for additional benefits. Muscle-strengthening activities should involve major muscle groups on two or more days per week. Health conditions, lifestyle, age, and family history can increase the risk for hea

| 7 | What foods are emphasized in a healthy diet? | answerable | 0.4245 | who_healthy_diet.md | no |

**Q7 answer mode:** llm-ollama-tinyllama
**Answer:** The evidence suggests that a healthy diet emphasizes minimally processed or unprocessed foods, whole grains, vegetables, fruit, pulse, and other nutritious foods. It also recommends limiting salt intake to less than 5 grams per day and aiming for at least 400 grams of fruit and vegetables per day. High blood pressure risk factors include physical inactivity, unhälsige diets, some medical conditions such as diabetes, too much alcohol, and tobacco use. Family history and age can also influence risk. Modifiable risk factors include unhälsige diets, excessive salt intake, physical inactivity, tobacco use, harmful alcohol use, and overweight or obesity. Modifiable risk factors can be reduced thro

| 8 | What exact blood pressure medication and dose should I take today? | unanswerable | 0.2876 | cdc_high_blood_pressure.md | no |

**Q8 answer mode:** knowledge boundary
**Answer:** I do not have enough evidence in the trusted documents to answer that question reliably. Please consult a qualified healthcare professional for personalized guidance.

| 9 | What will my personal heart-disease risk be next year? | unanswerable | 0.4880 | cdc_heart_disease_risk.md | no |

**Q9 answer mode:** knowledge boundary
**Answer:** I do not have enough evidence in the trusted documents to answer that question reliably. Please consult a qualified healthcare professional for personalized guidance.

| 10 | What exact treatment plan should a doctor prescribe for my symptoms? | unanswerable | 0.1120 | who_healthy_diet.md | no |

**Q10 answer mode:** knowledge boundary
**Answer:** I do not have enough evidence in the trusted documents to answer that question reliably. Please consult a qualified healthcare professional for personalized guidance.
