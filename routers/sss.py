import numpy as np
import matplotlib.pyplot as plt

from fastapi import APIRouter, HTTPException, status, Depends, Response

from common.cancer_types import CancerType, get_cancer_type, MachineType

from models import Appointment, Resource
from datetime import datetime

# create a day with 5 machines, 16*60 minutes
# 0 means no patient
# 1 means patient

day = np.zeros((5, 16*60))

class Eval:
    def __init__(self, calendar, shift_length = 4*60):
        self.calendar = calendar
        self.shift_length = shift_length
        self.TB_PREF = .38
        self.VB_PREF = .34
        self.U_PREF = .28



    
    def isOptimalArrangementOnDay(self, day_id, num_of_patients, all_treatment_time):
        # calculate ideal gaps
        ideal_gap_sizes = []

        # calculate actual gaps
        actual_gaps = []

        for machine, machine_index in self.calendar[day_id]:
            # calculate gaps for each machine
            ideal_gap_sizes[machine_index] = (DAY_MINUTE_SLOTS - all_treatment_time) / (num_of_patients + 1)

            gaps = []
            for i in range(DAY_MINUTE_SLOTS):
                if machine[i] == 0:
                    gaps[len(gaps) - 1] += 1
                else:
                    gaps.append(0)
            actual_gaps.append(gaps)

        gap_difs = []
        dif_avg = 1

        for machine, machine_index in self.calendar[day_id]:
            #calculate the difference between ideal and actual gaps
            gap_num_diff = num_of_patients + 1 - len(actual_gaps[machine_index])

            more_gap_count = num_of_patients + 1 + abs(gap_num_diff)

            difs = np.zeros(more_gap_count)

            for gap in range(more_gap_count):
                # find the smaller gap
                if ideal_gap_sizes[machine_index] < actual_gaps[0][machine_index]:
                    difs.append(1 - ideal_gap_sizes[machine_index] / actual_gaps[0][machine_index])
                    dif_avg *= difs[len(difs) - 1]
                else:
                    difs.append((actual_gaps[0][machine_index] / ideal_gap_sizes[machine_index]) - 1)
                    dif_avg *= difs[len(difs) - 1]

            gap_difs.append(difs)

        # calculate the avg of all difs
        dif_avg = 1 - dif_avg
        
        return dif_avg

    async def getMachineUsageRatio(self):
        machine_dict = {}
        machine_usages = np.zeros(5)

        for appointment in self.calendar:
            duration_minutes = int((appointment.end - appointment.start).total_seconds() / 60)
            machine_usages[appointment.resource_id - 1] += duration_minutes
            if appointment.resource_id - 1 not in machine_dict:
                machine_dict[appointment.resource_id - 1] = (await appointment.resource).type
                
        usage_sum = sum(machine_usages)

        machine_usage_JSON = []

        for i in range(len(machine_usages)):
            machine_usages[i] /= usage_sum
            machine_usage_JSON.append({
                "type": machine_dict[i],
                "usage": machine_usages[i]
            })

        print(machine_usage_JSON, "json")

        return machine_usage_JSON

    async def getMachinePref(self, machine_usages = None, cancer_type: CancerType = None):
        if machine_usages is None:
            print("machine usages is none")
            machine_usages = await self.getMachineUsageRatio()
            print(machine_usages, "machine usages")

        # machine usages type: {MachineType, usage}
        # order TB, TB, VB, VB, U
        actual_machine_prefs = []
        for machine in machine_usages:
            if machine["type"] == MachineType(MachineType.TRUEBEAM):
                actual_machine_prefs.append(self.TB_PREF - machine["usage"])
            elif machine["type"] == MachineType(MachineType.VITALBEAM):
                actual_machine_prefs.append(self.VB_PREF - machine["usage"])
            else:
                actual_machine_prefs.append(self.U_PREF - machine["usage"])

        return actual_machine_prefs
    


router = APIRouter(tags=["sss"])

@router.get("/")

async def get_sss():
    start_time = datetime(2023, 11, 25, 0, 0)
    end_time = datetime(2023, 11, 25, 23, 59)

    appointments_shift1 = await Appointment.filter(
        start__gte=start_time,
        start__lte=end_time,
    ).order_by('start')
    
    eval_current = Eval(appointments_shift1, 2*60)

    print(appointments_shift1[0].resource_id)


    print(await eval_current.getMachinePref())


    return "sss"