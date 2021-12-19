from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import json
import pandas as pd


columns = ["#", "Name", "Type1", "Type2", "Total", "Hp", "Attack", "Defense", "Sp_Atk", "Sp_Def", "Speed",
              "Generation", "Legendary"]
df = pd.read_csv('Pokemon.csv', names=columns)

is_legend = df.Legendary.to_list()
del is_legend[0]

name = df.Name.to_list()
del name[0]

type1 = df.Type1.to_list()
del type1[0]
type2 = df.Type2.to_list()
del type2[0]

size1 = len(type1)

strength = df.Total.to_list()
del strength[0]

gen = df.Generation.to_list()
del gen[0]

hp = df.Hp.to_list()
del hp[0]

speed = df.Speed.to_list()
del speed[0]

atk = df.Attack.to_list()
del atk[0]

defense = df.Defense.to_list()
del defense[0]

sp_atk = df.Sp_Atk.to_list()
del sp_atk[0]

sp_def = df.Sp_Def.to_list()
del sp_def[0]

# 注册一个事件响应器，事件类型为command
average_special_defense_pokemon = on_command("average_special_defense_pokemon", priority=2)
@average_special_defense_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(sp_def[i]) >= 65 and int(sp_def[i]) <= 100:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Average Special Defense Pokemon : " + to_json})


low_special_defense_pokemon = on_command("low_special_defense_pokemon", priority=2)
@low_special_defense_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(sp_def[i]) < 65:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Low Special Defense Pokemon : " + to_json})


high_special_defense_pokemon = on_command("high_special_defense_pokemon", priority=2)
@high_special_defense_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(sp_def[i]) > 100:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} High Special Defense Pokemon : " + to_json})


average_special_attack_pokemon = on_command("average_special_attack_pokemon", priority=2)
@average_special_attack_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(sp_atk[i]) >= 65 and int(sp_atk[i]) <= 100:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Average Special Attack Pokemon : " + to_json})


high_special_attack_pokemon = on_command("high_special_attack_pokemon", priority=2)
@high_special_attack_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(sp_atk[i]) >= 65 and int(sp_atk[i]) <= 100:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} High Special Attack Pokemon : " + to_json})


low_special_attack_pokemon = on_command("low_special_attack_pokemon", priority=2)
@low_special_attack_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(sp_atk[i]) < 65:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Low Special Attack Pokemon : " + to_json})



average_defense_pokemon = on_command("average_defense_pokemon", priority=2)
@average_defense_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(defense[i]) >= 65 and int(defense[i]) <= 100:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Average Defense Pokemon : " + to_json})



low_defense_pokemon = on_command("low_defense_pokemon", priority=2)
@low_defense_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(defense[i]) < 65:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Low Defense Pokemon : " + to_json})



high_defense_pokemon = on_command("high_defense_pokemon", priority=2)
@high_defense_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(defense[i]) > 100:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} High Defense Pokemon : " + to_json})


low_attack_pokemon = on_command("low_attack_pokemon", priority=2)
@low_attack_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(atk[i]) < 70:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Low Attack Pokemon : " + to_json})



average_attack_pokemon = on_command("average_attack_pokemon", priority=2)
@average_attack_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(atk[i]) >= 70 and int(atk[i]) <= 120:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Average Attack Pokemon : " + to_json})



high_attack_pokemon = on_command("high_attack_pokemon", priority=2)
@high_attack_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(atk[i]) > 120:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} High Attack Pokemon : " + to_json})



slow_pokemon = on_command("slow_pokemon", priority=2)
@slow_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(speed[i]) < 65:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Slow Pokemon : " + to_json})


average_speed_pokemon = on_command("average_speed_pokemon", priority=2)
@average_speed_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(speed[i]) >= 65 and int(speed[i]) <= 100:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Average Speed Pokemon : " + to_json})


fast_pokemon = on_command("fast_pokemon", priority=2)
@fast_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(speed[i]) > 100:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Fast Pokemon : " + to_json})


high_hp_pokemon = on_command("high_hp_pokemon", priority=2)
@high_hp_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(hp[i]) > 100:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} High Hp Pokemon : " + to_json})


low_hp_pokemon = on_command("low_hp_pokemon", priority=2)
@low_hp_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(hp[i]) < 70:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Low Hp Pokemon : " + to_json})


average_hp_pokemon = on_command("average_hp_pokemon", priority=2)
@average_hp_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if int(hp[i]) <= 100 and int(hp[i]) >= 70:
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Average Hp Pokemon : " + to_json})


pokemon_type = on_command("pokemon_type", priority=2)
@pokemon_type.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are 18 type of : fire, water, grass, ghost, dark, fighting, fairy, psychic, poison, flying, dragon, ice, ground, rock, steel, bug, electric, normal"})


pokemon_command = on_command("pokemon_command", priority=1)
@pokemon_command.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": "1.#legendary_pokemon " +
                                                                           " 2.#fire_type_pokemon" +
                                                                           " 3.#water_type_pokemon" +
                                                                           " 4.#grass_type_pokemon" +
                                                                           " 5.#electric_type_pokemon" +
                                                                           " 6.#poison_type_pokemon" +
                                                                           " 7.#dragon_type_pokemon" +
                                                                           " 8.#ice_type_pokemon" +
                                                                           " 9.#flying_type_pokemon" +
                                                                           " 10.#fairy_type_pokemon" +
                                                                           " 11.#fighting_type_pokemon" +
                                                                           " 12.#normal_type_pokemon" +
                                                                           " 13.#psychic_type_pokemon" +
                                                                           " 14.#dark_type_pokemon" +
                                                                           " 15.#ghost_type_pokemon" +
                                                                           " 16.#ground_type_pokemon" +
                                                                           " 17.#rock_type_pokemon" +
                                                                           " 18.#steel_type_pokemon" +
                                                                           " 19.#bug_type_pokemon" +
                                                                           " 20.#fast_pokemon" +
                                                                           " 21.#average_speed_pokemon" +
                                                                           " 22.#slow_pokemon" +
                                                                           " 23.#high_hp_pokemon" +
                                                                           " 24.#average_hp_pokemon" +
                                                                           " 25.#low_hp_pokemon" +
                                                                           " 26.#high_attack_pokemon" +
                                                                           " 27.#average_attack_pokemon" +
                                                                           " 28.#low_attack_pokemon" +
                                                                           " 29.#high_defense_pokemon" +
                                                                           " 30.#average_defense_pokemon" +
                                                                           " 31.#low_defense_pokemon" +
                                                                           " 32.#high_special_attack_pokemon" +
                                                                           " 33.#average_special_attack_pokemon" +
                                                                           " 34.#low_special_attack_pokemon" +
                                                                           " 35.#high_special_defense_pokemon" +
                                                                           " 36.#average_special_defense_pokemon" +
                                                                           " 37.#low_speical_defense_pokemon" +
                                                                           " 38.#gen1_pokemon" +
                                                                           " 39.#gen2_pokemon" +
                                                                           " 40.#gen3_pokemon" +
                                                                           " 41.#gen4_pokemon" +
                                                                           " 42.#gen5_pokemon" +
                                                                           " 43.#gen6_pokemon" +
                                                                           " 44.#pokemon_type" +
                                                                           " 45.#strong_pokemon" +
                                                                           " 46.#weak_pokemon" +
                                                                           " 47.#average_pokemon"})



gen1_pokemon = on_command("gen1_pokemon", priority=2)
@gen1_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if gen[i] == '1':
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Generation 1 Pokemon : " + to_json})


gen2_pokemon = on_command("gen2_pokemon", priority=2)
@gen2_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if gen[i] == '2':
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Generation 2 Pokemon : " + to_json})


gen3_pokemon = on_command("gen3_pokemon", priority=2)
@gen3_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if gen[i] == '3':
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Generation 3 Pokemon : " + to_json})


gen4_pokemon = on_command("gen4_pokemon", priority=2)
@gen4_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if gen[i] == '4':
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Generation 4 Pokemon : " + to_json})


gen5_pokemon = on_command("gen5_pokemon", priority=2)
@gen5_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if gen[i] == '5':
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Generation 5 Pokemon : " + to_json})


gen6_pokemon = on_command("gen6_pokemon", priority=2)
@gen6_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   g = ""
   for i in range(size1):
      if gen[i] == '6':
         g += name[i] + ", "
         count += 1
   to_json = json.dumps(g)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} Generation 6 Pokemon : " + to_json})


strong_pokemon = on_command("strong_pokemon", priority=2)
@strong_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   strong = ""
   for i in range(size1):
      if int(strength[i]) > 500:
         strong += name[i] + ", "
         count += 1
   to_json = json.dumps(strong)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} strong Pokemon : " + to_json})


weak_pokemon = on_command("weak_pokemon", priority=2)
@weak_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   weak = ""
   for i in range(size1):
      if int(strength[i]) < 350:
         weak += name[i] + ", "
         count += 1
   to_json = json.dumps(weak)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} weak Pokemon : " + to_json})


average_pokemon = on_command("average_pokemon", priority=2)
@average_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   average = ""
   for i in range(size1):
      if int(strength[i]) <= 500 and int(strength[i]) >= 350:
         average += name[i] + ", "
         count += 1
   to_json = json.dumps(average)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} average Pokemon : " + to_json})


legendary_pokemon = on_command("legendary_pokemon", priority=2)
@legendary_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   count = 0
   legend = ""
   for i in range(size1):
      if is_legend[i] != "False":
         legend += name[i] + ", "
         count += 1
   to_json = json.dumps(legend)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} lengdary Pokemon : " + to_json})


fire_type_pokemon = on_command("fire_type_pokemon", priority=3)
@fire_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Fire':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Fire':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} fire type Pokemon: " + to_json})


water_type_pokemon = on_command("water_type_pokemon", priority=4)
@water_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Water':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Water':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} water type Pokemon: " + to_json})


grass_type_pokemon = on_command("grass_type_pokemon", priority=5)
@grass_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Grass':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Grass':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} grass type Pokemon: " + to_json})


electric_type_pokemon = on_command("electric_type_pokemon", priority=6)
@electric_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Electric':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Electric':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} electric type Pokemon: " + to_json})


rock_type_pokemon = on_command("rock_type_pokemon", priority=7)
@rock_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Rock':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Rock':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} rock type Pokemon: " + to_json})


ground_type_pokemon = on_command("ground_type_pokemon", priority=8)
@ground_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Ground':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Ground':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} ground type Pokemon: " + to_json})


ghost_type_pokemon = on_command("ghost_type_pokemon", priority=9)
@ghost_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Ghost':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Ghost':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} ghost type Pokemon: " + to_json})


dark_type_pokemon = on_command("dark_type_pokemon", priority=10)
@dark_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Dark':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Dark':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} dark type Pokemon: " + to_json})


psychic_type_pokemon = on_command("psychic_type_pokemon", priority=11)
@psychic_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Psychic':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Psychic':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} psychic type Pokemon: " + to_json})


ice_type_pokemon = on_command("ice_type_pokemon", priority=12)
@ice_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Ice':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Ice':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} ice type Pokemon: " + to_json})


dragon_type_pokemon = on_command("dragon_type_pokemon", priority=13)
@dragon_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Dragon':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Dragon':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} dragon type Pokemon: " + to_json})


steel_type_pokemon = on_command("steel_type_pokemon", priority=14)
@steel_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Steel':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Steel':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} steel type Pokemon: " + to_json})


fairy_type_pokemon = on_command("fairy_type_pokemon", priority=15)
@fairy_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Fairy':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Fairy':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} fairy type Pokemon: " + to_json})


fighting_type_pokemon = on_command("fighting_type_pokemon", priority=16)
@fighting_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Fighting':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Fighting':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} fighting type Pokemon: " + to_json})


normal_type_pokemon = on_command("normal_type_pokemon", priority=17)
@normal_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Normal':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Normal':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} normal type Pokemon: " + to_json})


flying_type_pokemon = on_command("flying_type_pokemon", priority=18)
@flying_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Flying':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Flying':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} flying type Pokemon: " + to_json})


poison_type_pokemon = on_command("poison_type_pokemon", priority=19)
@poison_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Poison':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Poison':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} poison type Pokemon: " + to_json})


bug_type_pokemon = on_command("bug_type_pokemon", priority=20)
@bug_type_pokemon.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
   groupid = event.group_id
   element = ""
   count = 0
   for i in range(size1):
      if type1[i] == 'Bug':
         element += name[i] + ', '
         count += 1
      if type2[i] == 'Bug':
         element += name[i] + ', '
         count += 1
   to_json = json.dumps(element)
   await bot.call_api("send_group_msg", **{"group_id": groupid, "message": f"There are {count} bug type Pokemon: " + to_json})