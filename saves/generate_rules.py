import json

def generate():
    with open('save.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    detailed_descriptions = {
        1: "Компактне джерело безперебійного живлення постійного струму (DC UPS). Ідеально підходить для забезпечення безперервної роботи інтернет-маршрутизаторів (роутерів), ONU-терміналів оптоволокна та камер відеоспостереження під час короткочасних відключень.",
        2: "Потужний портативний акумулятор (Powerbank) з підтримкою швидкої зарядки (Power Delivery). Здатен кілька разів зарядити смартфон, планшет або підтримувати роботу ноутбука через Type-C протягом робочого дня.",
        3: "Готовий набір на базі свинцево-кислотного або гелевого акумулятора (12V) та енергоефективної LED-стрічки. Дозволяє освітити кімнату або невелике приміщення протягом багатьох годин.",
        4: "Класичний лінійно-інтерактивний ДБЖ (UPS), призначений для безпечного завершення роботи стаціонарного комп'ютера або збереження даних при раптовому зникненні напруги. Має вбудовану батарею на 10-15 хвилин автономії.",
        5: "Компактна портативна зарядна станція початкового рівня (близько 300 Вт·год). Має розетку 220В, USB-порти. Підходить для зарядки гаджетів, освітлення та живлення роутера, але не потягне потужну техніку.",
        6: "Комплект: компактна зарядна станція (до 300 Вт·год) та невелика складна сонячна панель (100 Вт). Дозволяє заряджати станцію вдень від сонця на балконі чи природі, забезпечуючи базову енергонезалежність.",
        7: "Універсальна портативна зарядна станція середньої ємності (500–800 Вт·год). Здатна заживити телевізор, комп'ютер, газовий котел (якщо підтримує чистий синус) протягом кількох годин.",
        8: "Комплект: зарядна станція середньої ємності (500–800 Вт·год) та портативна сонячна панель (160-220 Вт). Оптимальний баланс для тривалих відключень за умови доступу до сонця.",
        9: "Високопотужна зарядна станція (1000–1500 Вт·год). Може живити холодильник, мікрохвильовку, кавоварку або фен (короткочасно). Відмінно підходить для квартири під час тривалих відключень.",
        10: "Комплект: високопотужна зарядна станція (1000–1500 Вт·год) та сонячна панель (220-400 Вт). Дозволяє частково або повністю відновлювати заряд акумулятора протягом світлового дня.",
        11: "Преміальна зарядна станція високої ємності (2000–3600 Вт·год). Здатна забезпечити енергією майже всі прилади у квартирі, включаючи електрочайник, пральну машину або бойлер.",
        12: "Преміальна станція (2000–3600 Вт·год) з підключеною додатковою батареєю розширення, що подвоює ємність. Максимальний рівень автономії для квартири без використання генераторів.",
        13: "Бюджетна система: інвертор з правильною синусоїдою (300-500 Вт) та зовнішній GEL (гелевий) акумулятор (100Ah). Оптимальне рішення для тривалого живлення газового котла, циркуляційних насосів та освітлення.",
        14: "Надійна система: інвертор з правильною синусоїдою (1000 Вт) та сучасний LiFePO4 акумулятор (100Ah). Швидко заряджається, має великий ресурс (понад 3000 циклів) та високу безпеку.",
        15: "Бюджетний варіант автомобільного інвертора (чистий синус 1000 Вт), підключеного до автомобільного або тягового акумулятора. Потребує окремого зарядного пристрою та ручного керування.",
        16: "Гібридний інвертор (3 кВт, 24V) у поєднанні з акумулятором LiFePO4 (100Ah). Повноцінна система резервного живлення для квартири або невеликого будинку з можливістю підключення сонячних панелей.",
        17: "Потужний автономний інвертор (5 кВт, 48V) зі стійковим (серверним) акумулятором LiFePO4 на 5 кВт·год. Забезпечує безперебійне живлення всього будинку. Має високий рівень надійності.",
        18: "Комплексна настінна система акумулювання енергії (ESS) формату All-in-One. Інвертор та акумулятор (5-10 кВт·год) в одному естетичному корпусі. Преміальне рішення для сучасного будинку.",
        19: "Спеціалізоване ДБЖ подвійного перетворення (On-Line) на 1-2 кВт. Гарантує нульовий час перемикання та ідеальну якість напруги. Необхідно для серверів та чутливого медичного обладнання.",
        20: "Класичний бензиновий генератор відкритого типу (2.5 – 3 кВт). Простий та доступний в обслуговуванні. Достатньо для живлення базових приладів у будинку. Шумний та вимагає ручного запуску.",
        21: "Бензиновий генератор відкритого типу (2.5 – 3 кВт), оснащений блоком автоматичного введення резерву (ATS/АВР). Запускається самостійно при зникненні світла.",
        22: "Потужний бензиновий генератор (5 – 7 кВт). Здатен заживити потужні прилади: свердловинний насос, бойлер, електроплиту. Має значну вагу та високий рівень шуму.",
        23: "Потужний бензиновий генератор (5 – 7 кВт) з блоком автоматики (ATS/АВР). Забезпечує автоматичне перемикання живлення всього будинку при відключеннях.",
        24: "Інверторний бензиновий генератор закритого типу ('чемоданчик', до 2 кВт). Дуже тихий, економічний, видає чисту синусоїду. Ідеальний для виїздів або як резерв для котла на балконі (за умови відводу газів).",
        25: "Потужний інверторний генератор (3.5 – 4 кВт). Поєднує високу потужність, чисту напругу та помірний рівень шуму завдяки закритому корпусу та технології економії палива.",
        26: "Потужний інверторний генератор (3.5 – 4 кВт) з блоком автоматики (ATS/АВР). Преміальне автоматичне рішення для заміських будинків, чутливих до якості електроенергії.",
        27: "Двопаливний генератор (Газ/Бензин, 3 кВт). Може працювати як від бензину, так і від балона зі скрапленим газом (пропан-бутан). Газ забезпечує більшу економію та менше вихлопів.",
        28: "Двопаливний генератор (Газ/Бензин, 3 кВт) з блоком автоматики (ATS/АВР). Універсальне автоматичне рішення з можливістю вибору більш вигідного палива.",
        29: "Однофазний дизельний генератор (5 кВт). Відрізняється підвищеним моторесурсом та меншою витратою палива порівняно з бензиновими аналогами. Оптимальний для дуже частих та тривалих відключень.",
        30: "Однофазний дизельний генератор (5 кВт) з блоком автоматики (ATS/АВР). Надійна основа для резервного живлення будинку в умовах постійних блекаутів.",
        31: "Трифазний дизельний генератор (7–10 кВт). Призначений для живлення об'єктів з трифазним вводом та специфічним трифазним обладнанням (промислові насоси, верстати).",
        32: "Трифазний дизельний генератор (7–10 кВт) з блоком автоматики (ATS/АВР). Автоматичне професійне рішення для великих приватних будинків або комерційних об'єктів.",
        33: "Дизельний генератор у шумозахисному кожусі (5-10 кВт). Завдяки спеціальному корпусу працює значно тихіше за відкриті моделі, може встановлюватися поблизу житлових приміщень.",
        34: "Дизельний генератор у шумозахисному кожусі (5-10 кВт) з блоком автоматики (ATS/АВР). Максимальний комфорт, надійність та автоматизація для вимогливих користувачів.",
        35: "Мікроінверторна (балконна) сонячна електростанція (до 800 Вт). Складається з 1-2 панелей, що підключаються безпосередньо в розетку (On-Grid). Допомагає економити електроенергію вдень.",
        36: "Повноцінна гібридна сонячна електростанція (5 кВт). Включає інвертор, масив сонячних панелей на даху та блок акумуляторів. Забезпечує максимальну енергонезалежність та економію.",
        37: "Трифазна гібридна сонячна електростанція (понад 10 кВт). Промислове або преміальне приватне рішення для повного забезпечення великого об'єкта сонячною енергією та резервом."
    }

    for opt in data["options"]:
        opt_id = opt["id"]
        if opt_id in detailed_descriptions:
            opt["description"] = detailed_descriptions[opt_id]

    for q in data["questions"]:
        has_dk = any(a["value"] == "dk" for a in q["answers"])
        if not has_dk:
            q["answers"].append({"value": "dk", "label": "Не знаю"})

    opt_attrs = {}
    for i in range(1, 38):
        attrs = {
            "type": "battery",
            "fuel": False,
            "power": 0,
            "capacity": 0,
            "noise": "silent",
            "phase": 1,
            "automation": "none",
            "portability": "stationary",
            "pure_sine": True,
            "zero_transfer": False,
            "price_tier": "low"
        }
        
        if i in [1]: attrs.update({"power": 15, "capacity": 30, "price_tier": "low", "portability": "hand", "automation": "full"})
        if i in [2]: attrs.update({"power": 100, "capacity": 150, "price_tier": "low", "portability": "hand"})
        if i in [3]: attrs.update({"power": 50, "capacity": 200, "price_tier": "low", "portability": "hand"})
        if i in [4]: attrs.update({"power": 400, "capacity": 100, "price_tier": "low", "portability": "hand", "pure_sine": False, "automation": "full"})
        
        if i in [5, 6]: attrs.update({"power": 300, "capacity": 300, "price_tier": "mid", "portability": "hand", "automation": "avr"})
        if i in [7, 8]: attrs.update({"power": 800, "capacity": 700, "price_tier": "mid", "portability": "hand", "automation": "avr"})
        if i in [9, 10]: attrs.update({"power": 1500, "capacity": 1200, "price_tier": "high", "portability": "hand", "automation": "avr"})
        if i in [11, 12]: attrs.update({"power": 3000, "capacity": 3000, "price_tier": "premium", "portability": "wheels", "automation": "avr"})
        
        if i in [13]: attrs.update({"power": 500, "capacity": 1200, "price_tier": "mid", "portability": "stationary", "automation": "full"})
        if i in [14]: attrs.update({"power": 1000, "capacity": 1280, "price_tier": "high", "portability": "stationary", "automation": "full"})
        if i in [15]: attrs.update({"power": 1000, "capacity": 1200, "price_tier": "mid", "portability": "stationary"})
        if i in [16]: attrs.update({"power": 3000, "capacity": 2560, "price_tier": "high", "portability": "stationary", "automation": "full"})
        if i in [17, 18]: attrs.update({"power": 5000, "capacity": 5120, "price_tier": "premium", "portability": "stationary", "automation": "full"})
        if i in [19]: attrs.update({"power": 2000, "capacity": 1000, "price_tier": "high", "portability": "stationary", "automation": "full", "zero_transfer": True})
        
        if i in [20, 21]: attrs.update({"type": "generator", "fuel": True, "power": 3000, "noise": "loud", "price_tier": "mid", "portability": "wheels", "pure_sine": False})
        if i in [22, 23]: attrs.update({"type": "generator", "fuel": True, "power": 7000, "noise": "loud", "price_tier": "high", "portability": "wheels", "pure_sine": False})
        if i in [24]: attrs.update({"type": "generator", "fuel": True, "power": 2000, "noise": "quiet", "price_tier": "mid", "portability": "hand"})
        if i in [25, 26]: attrs.update({"type": "generator", "fuel": True, "power": 4000, "noise": "moderate", "price_tier": "high", "portability": "wheels"})
        if i in [27, 28]: attrs.update({"type": "generator", "fuel": True, "power": 3000, "noise": "loud", "price_tier": "high", "portability": "wheels", "pure_sine": False})
        if i in [29, 30]: attrs.update({"type": "generator", "fuel": True, "power": 5000, "noise": "loud", "price_tier": "high", "portability": "wheels", "pure_sine": False})
        if i in [31, 32]: attrs.update({"type": "generator", "fuel": True, "power": 10000, "noise": "loud", "price_tier": "premium", "portability": "stationary", "phase": 3, "pure_sine": False})
        if i in [33, 34]: attrs.update({"type": "generator", "fuel": True, "power": 10000, "noise": "moderate", "price_tier": "premium", "portability": "stationary"})
        
        if i in [35]: attrs.update({"type": "solar", "power": 800, "price_tier": "mid", "portability": "stationary"})
        if i in [36]: attrs.update({"type": "solar", "power": 5000, "capacity": 5000, "price_tier": "premium", "portability": "stationary", "automation": "full"})
        if i in [37]: attrs.update({"type": "solar", "power": 10000, "capacity": 10000, "price_tier": "premium", "portability": "stationary", "phase": 3, "automation": "full"})
        
        if i in [6, 8, 10]: attrs.update({"type": "battery_solar"})
        
        if i in [21, 23, 26, 28, 30, 32, 34]: attrs.update({"automation": "avr"})

        opt_attrs[i] = attrs

    new_rules = []
    
    def add(q, a, o, s):
        new_rules.append({"question_id": q, "answer_value": a, "option_id": o, "score_adjustment": float(s)})

    for o_id in range(1, 38):
        attrs = opt_attrs[o_id]
        
        if attrs["fuel"]: add(1, "a", o_id, -1000)
        elif attrs["type"] in ["solar", "battery_solar"]: add(1, "a", o_id, -1000)
        else: add(1, "a", o_id, 15 if attrs["portability"] == "hand" else 5)
        
        if attrs["fuel"] and o_id != 24: add(1, "b", o_id, -1000)
        elif o_id == 24: add(1, "b", o_id, -5)
        elif o_id in [35, 6, 8, 10]: add(1, "b", o_id, 15)
        else: add(1, "b", o_id, 5)

        if attrs["type"] in ["solar"]: add(1, "c", o_id, 15 if o_id in [36, 37] else 5)
        elif attrs["fuel"]: add(1, "c", o_id, 15)
        elif attrs["portability"] == "stationary": add(1, "c", o_id, 15)
        else: add(1, "c", o_id, 5)
        
        if attrs["automation"] in ["avr", "full"]: add(1, "d", o_id, 15)
        elif attrs["fuel"]: add(1, "d", o_id, -5)
        else: add(1, "d", o_id, 5)
        
        if attrs["portability"] == "hand": add(1, "e", o_id, 15)
        elif attrs["portability"] == "wheels": add(1, "e", o_id, -5)
        else: add(1, "e", o_id, -1000)

        tier = attrs["price_tier"]
        if tier == "low": add(2, "a", o_id, 15)
        elif tier == "mid": add(2, "a", o_id, -5)
        else: add(2, "a", o_id, -1000)
        if tier == "low": add(2, "b", o_id, 5)
        elif tier == "mid": add(2, "b", o_id, 15)
        elif tier == "high": add(2, "b", o_id, -5)
        else: add(2, "b", o_id, -1000)
        if tier == "mid": add(2, "c", o_id, 5)
        elif tier == "high": add(2, "c", o_id, 15)
        elif tier == "low": add(2, "c", o_id, -5)
        elif tier == "premium": add(2, "c", o_id, -5)
        if tier == "high": add(2, "d", o_id, 15)
        elif tier == "premium": add(2, "d", o_id, 5)
        elif tier == "mid": add(2, "d", o_id, 0)
        elif tier == "low": add(2, "d", o_id, 0)
        if tier == "premium": add(2, "e", o_id, 15)
        elif tier == "high": add(2, "e", o_id, 5)
        else: add(2, "e", o_id, 0)

        p = attrs["power"]
        if p < 500: add(3, "a", o_id, 15)
        elif p <= 2000: add(3, "a", o_id, 5)
        else: add(3, "a", o_id, -5)
        
        if p < 500: add(3, "b", o_id, -1000)
        elif 500 <= p <= 2000: add(3, "b", o_id, 15)
        else: add(3, "b", o_id, 5)
        
        if p < 1500: add(3, "c", o_id, -1000)
        elif 1500 <= p < 3000: add(3, "c", o_id, 5)
        else: add(3, "c", o_id, 15)
        
        if p < 3500: add(3, "d", o_id, -1000)
        elif 3500 <= p < 5000: add(3, "d", o_id, 5)
        else: add(3, "d", o_id, 15)

        c = attrs["capacity"]
        fuel = attrs["fuel"]
        
        if o_id == 35:
            add(4, "a", o_id, -1000)
            add(4, "b", o_id, -1000)
            add(4, "c", o_id, -1000)
            add(4, "d", o_id, -1000)
        else:
            if fuel: add(4, "a", o_id, 5)
            elif c < 300: add(4, "a", o_id, 15)
            elif 300 <= c < 1500: add(4, "a", o_id, 5)
            else: add(4, "a", o_id, -5)
    
            if fuel: add(4, "b", o_id, 15)
            elif c < 300: add(4, "b", o_id, -5)
            elif 300 <= c <= 1500: add(4, "b", o_id, 15)
            else: add(4, "b", o_id, 5)
    
            if fuel: add(4, "c", o_id, 15)
            elif c < 800: add(4, "c", o_id, -1000)
            elif 800 <= c < 2500: add(4, "c", o_id, 5)
            else: add(4, "c", o_id, 15)
    
            if fuel or attrs["type"] in ["solar", "battery_solar"]: 
                add(4, "d", o_id, 15)
            elif c >= 3000: 
                add(4, "d", o_id, 5)
            else: 
                add(4, "d", o_id, -5)

        if fuel:
            add(5, "a", o_id, -1000)
            if o_id in [27, 28, 24]: add(5, "b", o_id, 15)
            else: add(5, "b", o_id, -5)
            add(5, "c", o_id, 15)
        else:
            add(5, "a", o_id, 15)
            add(5, "b", o_id, 15)
            add(5, "c", o_id, 5)

        auto = attrs["automation"]
        if auto in ["avr", "full"]:
            add(6, "a", o_id, 15)
            add(6, "b", o_id, 5)
            add(6, "c", o_id, 5)
        else:
            add(6, "a", o_id, -1000)
            add(6, "b", o_id, 15 if attrs["portability"] == "stationary" else 5)
            add(6, "c", o_id, 15)

        noise = attrs["noise"]
        if noise == "silent": add(7, "a", o_id, 15)
        elif noise == "quiet": add(7, "a", o_id, -5)
        else: add(7, "a", o_id, -1000)
        if noise in ["silent", "quiet"]: add(7, "b", o_id, 15)
        elif noise == "moderate": add(7, "b", o_id, -5)
        else: add(7, "b", o_id, -1000)
        if noise in ["moderate", "quiet", "silent"]: add(7, "c", o_id, 15)
        else: add(7, "c", o_id, -5)
        add(7, "d", o_id, 15 if noise == "loud" else 5)

        phase = attrs["phase"]
        if phase == 1:
            add(8, "a", o_id, 15)
            add(8, "b", o_id, -1000)
            add(8, "c", o_id, 15)
        else:
            add(8, "a", o_id, -1000)
            add(8, "b", o_id, 15)
            add(8, "c", o_id, 5)

        stype = attrs["type"]
        if stype in ["solar", "battery_solar"]:
            add(9, "a", o_id, -1000)
            if o_id in [6, 8, 10, 35]: add(9, "b", o_id, 15)
            else: add(9, "b", o_id, -1000)
            add(9, "c", o_id, 15)
        else:
            add(9, "a", o_id, 15)
            add(9, "b", o_id, 5)
            add(9, "c", o_id, 5)

        port = attrs["portability"]
        if port == "hand":
            add(10, "a", o_id, 15)
            add(10, "b", o_id, 5)
            add(10, "c", o_id, -1000)
            add(10, "d", o_id, 15)
        elif port == "wheels":
            add(10, "a", o_id, -1000)
            add(10, "b", o_id, 15)
            add(10, "c", o_id, -5)
            add(10, "d", o_id, 15)
        else:
            add(10, "a", o_id, -1000)
            add(10, "b", o_id, -1000)
            add(10, "c", o_id, 15)
            add(10, "d", o_id, 15)

        pure = attrs["pure_sine"]
        zero = attrs["zero_transfer"]
        obj_type = attrs["type"]
        
        if pure:
            add(11, "a", o_id, 5)
            if zero:
                add(11, "b", o_id, 5)
                add(11, "c", o_id, 15)
            else:
                add(11, "b", o_id, 15)
                add(11, "c", o_id, -5)
        else:
            add(11, "a", o_id, 15)
            
            if obj_type == "generator":
                add(11, "b", o_id, -5) 
                add(11, "c", o_id, -5) 
            else:
                add(11, "b", o_id, -1000)
                add(11, "c", o_id, -1000)

        if port == "hand":
            add(12, "a", o_id, 15)
            add(12, "b", o_id, 5)
            add(12, "c", o_id, -5)
            add(12, "d", o_id, 15)
        elif port == "wheels":
            if attrs["automation"] == "avr":
                add(12, "a", o_id, -1000)
                add(12, "b", o_id, 15)
            else:
                add(12, "a", o_id, 5)
                add(12, "b", o_id, 15)
            add(12, "c", o_id, -5)
            add(12, "d", o_id, 15)
        else:
            if o_id == 35:
                add(12, "a", o_id, 15)
                add(12, "b", o_id, -1000) 
            else:
                add(12, "a", o_id, -1000)
                add(12, "b", o_id, 15 if attrs["type"] != "solar" else -5)
            add(12, "c", o_id, 15)
            add(12, "d", o_id, 15)

    for o_id in range(1, 38):
        for q_id in range(1, 13):
            add(q_id, "dk", o_id, 0.0)

    data["rules"] = new_rules

    print(f"Generated {len(new_rules)} rules.")

    with open('save.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generate()
