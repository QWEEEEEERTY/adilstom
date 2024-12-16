from datetime import datetime


def merge_adjacent(schedule: [str]) -> [str]:
    if not schedule:
        return []
    schedule.sort()
    merged_schedule = []
    prev_start, prev_end = schedule[0].split('-')

    for time_slot in schedule[1:]:
        start, end = time_slot.split('-')
        if prev_end == start:
            prev_end = end
        else:
            merged_schedule.append(f"{prev_start}-{prev_end}")
            prev_start, prev_end = start, end

    merged_schedule.append(f"{prev_start}-{prev_end}")
    return merged_schedule


def get_free_time(schedule: [str], work_start: str = "10:00", work_end: str = "19:00", min_interval: int = 40) -> [str]:
    free_schedule = []
    prev_end = work_start

    for time_slot in schedule:
        start, end = time_slot.split('-')
        if prev_end < start:
            free_time = get_time_difference(prev_end, start)
            if free_time >= min_interval:
                free_schedule.append(f"{prev_end}-{start}")
        prev_end = end
    if prev_end < work_end:
        free_time = get_time_difference(prev_end, work_end)
        if free_time >= 40:
            free_schedule.append(f"{prev_end}-{work_end}")

    return free_schedule


def get_time_difference(start: str, end: str) -> int:
    fmt = "%H:%M"
    start_dt = datetime.strptime(start, fmt)
    end_dt = datetime.strptime(end, fmt)
    return int((end_dt - start_dt).total_seconds() // 60)


def get_doctors(response: dict, date: str):
    doctors = {}
    for doctor in response.values():
        if doctor[date]:
            doctor_id = doctor[date][0]["doctor"]
            doctor_name = doctor[date][0]["doctorName"]
            doctors[doctor_id] = {
                "name": doctor_name,
                "schedule": []
            }
    return doctors


def get_schedule(response: dict, doctors: dict, date: str) -> dict:
    if not response:
        return doctors
    for patient in response[date]:
        if patient["item"]["status"] == "2":
            continue
        start_time = patient["start"].split()[-1][:5]
        end_time = patient["end"].split()[-1][:5]
        doctors[patient["docId"]]["schedule"].append(f"{start_time}-{end_time}")
    return doctors


def parse_schedule(response: dict, date: str) -> dict:
    doctors = get_doctors(response.get("rasp"), date)
    doctors = get_schedule(response.get("schedule"), doctors, date)
    for doctor_info in doctors.values():
        doctor_info["schedule"] = merge_adjacent(doctor_info["schedule"])
        doctor_info["schedule"] = get_free_time(doctor_info["schedule"])

    return doctors
