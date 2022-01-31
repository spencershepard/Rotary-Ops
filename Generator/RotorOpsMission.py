from tokenize import String

import dcs
import os
import random
import RotorOpsUnits
import time


class RotorOpsMission:


    conflict_zones = {}
    staging_zones = {}
    spawn_zones = {}
    scripts = {}


    def __init__(self):
        self.m = dcs.mission.Mission()
        self.old_blue = self.m.coalition.get("blue").dict()
        self.old_red = self.m.coalition.get("red").dict()
        os.chdir("../")
        self.home_dir = os.getcwd()
        self.scenarios_dir = self.home_dir + "\Generator\Scenarios"
        self.forces_dir = self.home_dir + "\Generator\Forces"
        self.script_directory = self.home_dir
        self.sound_directory = self.home_dir + "\sound\embedded"
        self.output_dir = self.home_dir + "\Generator\Output"
        self.assets_dir = self.home_dir + "\Generator/assets"


    class RotorOpsZone:
        def __init__(self, name: str, flag: int, position: dcs.point, size: int):
            self.name = name
            self.flag = flag
            self.position = position
            self.size = size

    def getMission(self):
        return self.m

    def addZone(self, zone_dict, zone: RotorOpsZone):
        zone_dict[zone.name] = zone

    def addResources(self, sound_directory, script_directory):
        # add all of our required sounds
        os.chdir(sound_directory)
        path = os.getcwd()
        dir_list = os.listdir(path)
        # print("Files and directories in '", path, "' :")
        # print(dir_list)

        for filename in dir_list:
            if filename.endswith(".ogg"):
                #print(filename)
                self.m.map_resource.add_resource_file(filename)

        #add all of our lua scripts
        os.chdir(script_directory)
        path = os.getcwd()
        dir_list = os.listdir(path)
        # print("Files and directories in '", path, "' :")
        # print(dir_list)

        for filename in dir_list:
            if filename.endswith(".lua"):
                print("Adding script to mission: " + filename)
                self.scripts[filename] = self.m.map_resource.add_resource_file(filename)

    def getUnitsFromMiz(self, filename, side):
        forces = []
        os.chdir(self.home_dir)
        os.chdir(self.forces_dir + "/" + side)
        print("Looking for " + side + " Forces files in '", os.getcwd(), "' :")
        source_mission = dcs.mission.Mission()
        try:
            source_mission.load_file(filename)

            for country_name in source_mission.coalition.get(side).countries:
                country_obj = source_mission.coalition.get(side).countries[country_name]
                for vehicle_group in country_obj.vehicle_group:
                    forces.append(vehicle_group)
            return forces
        except:
            print("Failed to load units from " + filename)


    def generateMission(self, options):
        #get the template mission file

        os.chdir(self.scenarios_dir)
        print("Looking for mission files in '", os.getcwd(), "' :")

        self.m.load_file(options["scenario_filename"])

        #Load the default coalitions for simplicity
        self.m.coalition.get("blue").load_from_dict(self.m, self.old_blue)
        self.m.coalition.get("red").load_from_dict(self.m, self.old_red)


        red_forces = self.getUnitsFromMiz(options["red_forces_filename"], "red")
        blue_forces = self.getUnitsFromMiz(options["blue_forces_filename"], "blue")



        # add zones to target mission
        for zone in self.m.triggers.zones():
            if zone.name == "ALPHA":
                self.addZone(self.conflict_zones, self.RotorOpsZone("ALPHA", 101, zone.position, zone.radius))
            elif zone.name == "BRAVO":
                self.addZone(self.conflict_zones, self.RotorOpsZone("BRAVO", 102, zone.position, zone.radius))
            elif zone.name == "CHARLIE":
                self.addZone(self.conflict_zones, self.RotorOpsZone("CHARLIE", 103, zone.position, zone.radius))
            elif zone.name == "DELTA":
                self.addZone(self.conflict_zones, self.RotorOpsZone("DELTA", 104, zone.position, zone.radius))
            elif zone.name.rfind("STAGING") >= 0:
                self.addZone(self.staging_zones, self.RotorOpsZone(zone.name, None, zone.position, zone.radius))
            elif zone.name.rfind("SPAWN") >= 0:
                self.addZone(self.spawn_zones, self.RotorOpsZone(zone.name, None, zone.position, zone.radius))

        #add files and triggers necessary for RotorOps.lua script
        self.addResources(self.sound_directory, self.script_directory)
        self.scriptTriggerSetup(options)

        blue_zones = self.staging_zones
        red_zones = self.conflict_zones
        if options["defending"]:
            blue_zones = self.conflict_zones
            red_zones = self.staging_zones
            #swap airport sides
            blue_airports = self.getCoalitionAirports("blue")
            red_airports = self.getCoalitionAirports("red")
            for airport_name in blue_airports:
                self.m.terrain.airports[airport_name].set_red()
            for airport_name in red_airports:
                self.m.terrain.airports[airport_name].set_blue()


        #Add red ground units
        for zone_name in red_zones:
            if red_forces:
                    self.addGroundGroups(red_zones[zone_name], self.m.country('Russia'), red_forces, options["red_quantity"])

        #Add blue ground units
        for zone_name in blue_zones:
            if blue_forces:
                self.addGroundGroups(blue_zones[zone_name], self.m.country('USA'), blue_forces,
                                     options["blue_quantity"])

        #Add player slots
        if options["slots"] == "Multiple Slots":
            self.addMultiplayerHelos()
        else:
            for helicopter in dcs.helicopters.helicopter_map:
                if helicopter == options["slots"]:
                    self.addSinglePlayerHelos(dcs.helicopters.helicopter_map[helicopter])

        self.addFlights(options)

        #Set the Editor Map View
        self.m.map.position = self.m.terrain.airports[self.getCoalitionAirports("blue")[0]].position
        self.m.map.zoom = 100000

        #Save the mission file
        print(self.m.triggers.zones())
        os.chdir(self.output_dir)
        output_filename = options["scenario_filename"].removesuffix('.miz') + " " + time.strftime('%a%H%M%S') + '.miz'
        success = self.m.save(output_filename)
        return {"success": success, "filename": output_filename, "directory": self.output_dir} #let the UI know the result

    def addGroundGroups(self, zone, _country, groups, quantity):
        for a in range(0, quantity):

            group = random.choice(groups)
            unit_types = []
            for unit in group.units:
                if dcs.vehicles.vehicle_map[unit.type]:
                    unit_types.append(dcs.vehicles.vehicle_map[unit.type])
            country = self.m.country(_country.name)
            pos1 = zone.position.point_from_heading(5, 500)
            #for i in range(0, quantity):
            self.m.vehicle_group_platoon(
                country,
                zone.name + '-GND ' + str(a+1),
                unit_types,
                pos1.random_point_within(zone.size / 2, 500),
                heading=random.randint(0, 359),
                formation=dcs.unitgroup.VehicleGroup.Formation.Scattered,
            )

    def getCoalitionAirports(self, side: str):
        coalition_airports = []
        for airport_name in self.m.terrain.airports:
            airportobj = self.m.terrain.airports[airport_name]
            if airportobj.coalition == str.upper(side):
                coalition_airports.append(airport_name)
        return coalition_airports


    def addSinglePlayerHelos(self, helotype):
        friendly_airports = self.getCoalitionAirports("blue")
        for airport_name in friendly_airports:
            fg = self.m.flight_group_from_airport(self.m.country('USA'), "Player Helos", helotype,
                                                  self.m.terrain.airports[airport_name], group_size=2)
            fg.units[0].set_player()


    def addMultiplayerHelos(self):
        friendly_airports = self.getCoalitionAirports("blue")
        for airport_name in friendly_airports:
            for helotype in RotorOpsUnits.client_helos:
                fg = self.m.flight_group_from_airport(self.m.country('USA'), airport_name + " " + helotype.id, helotype,
                                                      self.m.terrain.airports[airport_name], group_size=1)
                fg.units[0].set_client()


    class TrainingScenario():
        @staticmethod
        def random_orbit(rect: dcs.mapping.Rectangle):
            x1 = random.randrange(int(rect.bottom), int(rect.top))
            sy = rect.left
            y1 = random.randrange(int(sy), int(rect.right))
            heading = 90 if y1 < (sy + (rect.right - sy) / 2) else 270
            heading = random.randrange(heading - 20, heading + 20)
            race_dist = random.randrange(80 * 1000, 120 * 1000)
            return dcs.mapping.Point(x1, y1), heading, race_dist



    def addFlights(self, options):
        usa = self.m.country(dcs.countries.USA.name)
        russia = self.m.country(dcs.countries.Russia.name)
        friendly_airport = self.m.terrain.airports[self.getCoalitionAirports("blue")[0]]
        enemy_airport = self.m.terrain.airports[self.getCoalitionAirports("red")[0]]


        orbit_rect = dcs.mapping.Rectangle(
            int(friendly_airport.position.x), int(friendly_airport.position.y - 100 * 1000), int(friendly_airport.position.x - 100 * 1000),
            int(friendly_airport.position.y))

        if options["f_awacs"]:
            awacs_name = "AWACS"
            awacs_freq = 266
            pos, heading, race_dist = self.TrainingScenario.random_orbit(orbit_rect)
            awacs = self.m.awacs_flight(
                usa,
                awacs_name,
                plane_type=dcs.planes.E_3A,
                airport=None,
                position=pos,
                race_distance=race_dist, heading=heading,
                altitude=random.randrange(4000, 5500, 100), frequency=awacs_freq)

            awacs_escort = self.m.escort_flight(usa, "AWACS Escort", dcs.countries.USA.Plane.F_15C, None, awacs, group_size=2)
            awacs_escort.load_loadout("Combat Air Patrol") #not working for f-15
            briefing = self.m.description_text() + "\n\n" + awacs_name + "  " + str(awacs_freq) + ".00 " + "\n"
            self.m.set_description_text(briefing)

        if options["f_tankers"]:
            t1_name = "Tanker KC_130 Basket"
            t1_freq = 253
            t1_tac = "61Y"
            t2_name = "Tanker KC_135 Boom"
            t2_freq = 256
            t2_tac = "101Y"
            pos, heading, race_dist = self.TrainingScenario.random_orbit(orbit_rect)
            refuel_net = self.m.refuel_flight(
                usa,
                t1_name,
                dcs.planes.KC130,
                airport=None,
                position=pos,
                race_distance=race_dist, heading=heading,
                altitude=random.randrange(4000, 5500, 100), speed=750, frequency=t1_freq, tacanchannel=t1_tac)

            pos, heading, race_dist = self.TrainingScenario.random_orbit(orbit_rect)
            refuel_rod = self.m.refuel_flight(
                usa,
                t2_name,
                dcs.planes.KC_135,
                airport=None,
                position=pos,
                race_distance=race_dist, heading=heading,
                altitude=random.randrange(4000, 5500, 100), frequency=t2_freq, tacanchannel=t2_tac)

            briefing = self.m.description_text() + "\n\n" + t1_name + "  " + str(t1_freq) + ".00  " + t1_tac + "\n" + t2_name + "  " + str(t2_freq) + ".00  " + t2_tac + "\n"
            self.m.set_description_text(briefing)

        def zone_attack(fg, unit_type):
            fg.set_skill(dcs.unit.Skill.Random)
            fg.late_activation = True
            #fg.load_loadout(unit_type["loadout"])
            #task = dcs.task.CAS
            #loadout = dcs.planes.Su_25.loadout(task)
            #loadout = dcs.planes.Su_25.loadout_by_name("Ground Attack")
            #fg.load_task_default_loadout(task)
            #fg.load_loadout("Ground Attack")
            #fg.load_task_default_loadout(dcs.task.GroundAttack)

            #fg.load_loadout("2xB-13L+4xATGM 9M114")
            if options["defending"]:
                for zone_name in self.conflict_zones:
                    fg.add_waypoint(self.conflict_zones[zone_name].position, 1000)
            else:
                for zone_name in reversed(self.conflict_zones):
                    fg.add_waypoint(self.conflict_zones[zone_name].position, 1000)
            fg.add_runway_waypoint(enemy_airport)
            fg.land_at(enemy_airport)

        if options["e_attack_helos"]:
            helo = random.choice(RotorOpsUnits.e_attack_helos)
            afg = self.m.flight_group_from_airport(
                russia,
                "Enemy Attack Helicopters",
                helo,
                airport=enemy_airport,
                maintask=dcs.task.GroundAttack,
                start_type=dcs.mission.StartType.Warm,
                group_size=2)
            zone_attack(afg, helo)

        if options["e_attack_planes"]:
            plane = random.choice(RotorOpsUnits.e_attack_planes)
            afg = self.m.flight_group_from_airport(
                russia, "Enemy Attack Planes", plane["type"],
               airport=enemy_airport,
               maintask=dcs.task.GroundAttack,
               start_type=dcs.mission.StartType.Warm,
               group_size=2)
            zone_attack(afg, plane)


    def scriptTriggerSetup(self, options):

        #get the boolean value from ui option and convert to lua string
        def lb(var):
            return str(options[var]).lower()

        game_flag = 100
        #Add the first trigger
        mytrig = dcs.triggers.TriggerOnce(comment="RotorOps Setup Scripts")
        mytrig.rules.append(dcs.condition.TimeAfter(1))
        mytrig.actions.append(dcs.action.DoScriptFile(self.scripts["mist_4_4_90.lua"]))
        mytrig.actions.append(dcs.action.DoScriptFile(self.scripts["Splash_Damage_2_0.lua"]))
        mytrig.actions.append(dcs.action.DoScriptFile(self.scripts["CTLD.lua"]))
        mytrig.actions.append(dcs.action.DoScriptFile(self.scripts["RotorOps.lua"]))
        mytrig.actions.append(dcs.action.DoScript(dcs.action.String((
            "--OPTIONS HERE!\n\n" +
            "RotorOps.CTLD_crates = " + lb("crates") + "\n\n" +
            "RotorOps.CTLD_sound_effects = true\n\n" +
            "RotorOps.force_offroad = " + lb("force_offroad") + "\n\n" +
            "RotorOps.voice_overs = " + lb("voiceovers") + "\n\n" +
            "RotorOps.zone_status_display = " + lb("game_display") + "\n\n" +
            "RotorOps.inf_spawns_per_zone = " + lb("inf_spawn_qty") + "\n\n" +
            "RotorOps.apcs_spawn_infantry = " + lb("apc_spawns_inf") + " \n\n"))))
        self.m.triggerrules.triggers.append(mytrig)

        #Add the second trigger
        mytrig = dcs.triggers.TriggerOnce(comment="RotorOps Setup Zones")
        mytrig.rules.append(dcs.condition.TimeAfter(2))
        for s_zone in self.staging_zones:
            mytrig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.stagingZone('" + s_zone + "')")))
        for c_zone in self.conflict_zones:
            zone_flag = self.conflict_zones[c_zone].flag
            mytrig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.addZone('" + c_zone + "'," + str(zone_flag) + ")")))

        mytrig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.setupConflict('" + str(game_flag) + "')")))

        self.m.triggerrules.triggers.append(mytrig)

        #Add the third trigger
        mytrig = dcs.triggers.TriggerOnce(comment="RotorOps Conflict Start")
        mytrig.rules.append(dcs.condition.TimeAfter(10))
        mytrig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.startConflict(100)")))
        self.m.triggerrules.triggers.append(mytrig)

        #Add all zone-based triggers
        for index, c_zone in enumerate(self.conflict_zones):

            z_active_trig = dcs.triggers.TriggerOnce(comment= c_zone + " Active")
            z_active_trig.rules.append(dcs.condition.FlagEquals(game_flag, index + 1))
            z_active_trig.actions.append(dcs.action.DoScript(dcs.action.String("--Add any action you want here!")))
            self.m.triggerrules.triggers.append(z_active_trig)

            zone_flag = self.conflict_zones[c_zone].flag
            z_weak_trig = dcs.triggers.TriggerOnce(comment= c_zone + " Weak")
            z_weak_trig.rules.append(dcs.condition.FlagIsMore(zone_flag, 10))
            z_weak_trig.rules.append(dcs.condition.FlagIsLess(zone_flag, random.randrange(20, 80)))
            z_weak_trig.actions.append(dcs.action.DoScript(dcs.action.String("--Add any action you want here!\n\n--Flag value represents the percentage of defending ground units remaining. ")))
            if options["e_attack_helos"]:
                z_weak_trig.actions.append(dcs.action.DoScript(dcs.action.String("mist.respawnGroup('Enemy Attack Helicopters', true)")))
            self.m.triggerrules.triggers.append(z_weak_trig)

        #Add game won/lost triggers
        mytrig = dcs.triggers.TriggerOnce(comment="RotorOps Conflict WON")
        mytrig.rules.append(dcs.condition.FlagEquals(game_flag, 99))
        mytrig.actions.append(dcs.action.DoScript(dcs.action.String("---Add an action you want to happen when the game is WON")))
        self.m.triggerrules.triggers.append(mytrig)

        mytrig = dcs.triggers.TriggerOnce(comment="RotorOps Conflict LOST")
        mytrig.rules.append(dcs.condition.FlagEquals(game_flag, 98))
        mytrig.actions.append(dcs.action.DoScript(dcs.action.String("---Add an action you want to happen when the game is LOST")))
        self.m.triggerrules.triggers.append(mytrig)


