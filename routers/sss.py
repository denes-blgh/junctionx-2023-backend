import numpy as np
import matplotlib.pyplot as plt

from fastapi import APIRouter, HTTPException, status, Depends, Response

from common.cancer_types import CancerType, get_cancer_type, MachineType

from models import Appointment, Resource
from datetime import datetime

from build.utils import Machine, schedule
from build.utils import Appointment as AppointmentBind
from build.utils import Demand as DemandBind

# create a day with 5 machines, 16*60 minutes
# 0 means no patient
# 1 means patient

np.set_printoptions(precision=2)

class Eval:
    async def __init__(self, calendar, shift_length = 4*60, reserve_ratio = .8):
        self.calendar = calendar
        self.shift_length = shift_length
        self.TB_PREF = .38
        self.VB_PREF = .34
        self.U_PREF = .28
        self.reserve_ratio = reserve_ratio

        self.machines = []
        for resource in await Resource.all():
            self.machines.append(Machine(resource.id, resource.type))

    
    async def isOptimalArrangementOnDay(self):
        num_of_patients = len(self.calendar)

        print(num_of_patients, "num of patients")

        result = schedule(
            self.machines, 
            self.shift_length, 
            self.reserve_ratio
        )

        print(result, "result")

        all_treatment_time = await self.getMachineUsages()

        print(all_treatment_time, "all treatment time")

        calendar_by_machine = sorted(self.calendar, key=lambda appointment: appointment.resource_id)
        
        # calculate ideal gaps
        ideal_gap_sizes = np.zeros(5)

        # calculate actual gaps
        actual_gaps = [[] for _ in range(5)]

        for machine_index in range(len(self.calendar)):
            current_appointment = self.calendar[machine_index]

            # calculate gaps for each machine
            if ideal_gap_sizes[current_appointment.resource_id - 1] == 0:
                ideal_gap_sizes[current_appointment.resource_id - 1] = (self.shift_length - all_treatment_time[current_appointment.resource_id - 1]) / (num_of_patients + 1)

            # calculate actual gaps
            if machine_index < len(self.calendar) - 1:
                next_appointment = self.calendar[machine_index + 1]
                if next_appointment.resource_id == current_appointment.resource_id:
                    actual_gaps[current_appointment.resource_id - 1].append((next_appointment.start - current_appointment.end).total_seconds() / 60)



        print(ideal_gap_sizes)

        print(actual_gaps)

        gap_difs = []
        dif_avg = 1

        for machine_index in range(5):
            if len(actual_gaps[machine_index]) < num_of_patients:
                more_gap_count = num_of_patients
            else:
                more_gap_count = len(actual_gaps[machine_index]) - 1

            difs = []

            for gap in range(more_gap_count):
                # find the smaller gap
                print(actual_gaps, "csa")
                if ideal_gap_sizes[machine_index] < actual_gaps[machine_index][gap]:
                    difs.append(1 - ideal_gap_sizes[machine_index] / actual_gaps[0][machine_index])
                    dif_avg *= difs[len(difs) - 1]
                else:
                    difs.append((actual_gaps[0][machine_index] / ideal_gap_sizes[machine_index]) - 1)
                    dif_avg *= difs[len(difs) - 1]

            gap_difs.append(difs)

        print(gap_difs)

        # calculate the avg of all difs
        dif_avg = 1 - dif_avg
        
        return dif_avg

    async def getMachineUsages(self):
        machine_usages = np.zeros(5)

        for appointment in self.calendar:
            duration_minutes = int((appointment.end - appointment.start).total_seconds() / 60)
            machine_usages[appointment.resource_id - 1] += duration_minutes
                
        return machine_usages

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

        return machine_usage_JSON

    async def getMachinePref(self, machine_usages = None, cancer_type: CancerType = None):
        if machine_usages is None:
            print("machine usages is none")
            machine_usages = await self.getMachineUsageRatio()

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
async def insert_urgent(demand, urgent_appointment_date):
    return "vrrrram"

@router.get("/rearrange")
async def rearrange(account_id, appointments):
    return "csikao"

async def new_appointment(demand):
    return "jihau"