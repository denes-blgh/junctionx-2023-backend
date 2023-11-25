#include <bits/stdc++.h>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

namespace py = pybind11;

struct Machine
{
    int id;
    std::string type;

    Machine (const int id, const std::string_view type) 
    : id(id), type(type) 
    {}
};

struct Demand
{
    int id, fractions, duration;
    bool is_inpatient;
    std::vector<std::string> machine_options;

    Demand (
        const int id, 
        const int fractions, 
        const int duration,
        const bool is_inpatient, 
        const std::vector<std::string> &machine_options
    )
    :   id(id), 
        fractions(fractions), 
        duration(duration),
        is_inpatient(is_inpatient), 
        machine_options(machine_options)
    {}
};

struct Appointment
{
    int demand_id, machine_id, day, start, duration;

    Appointment (
        const int demand_id, 
        const int machine_id,
        const int day, // index of day
        const int start, // minutes from the start of the day
        const int duration // treatment duration in minutes
    )
    :   demand_id(demand_id), 
        machine_id(machine_id), 
        day(day),
        start(start),
        duration(duration)
    {}
};

struct Utilization
{
    std::vector<Demand *> reservations;
    size_t total = 0;
};

struct Frame
{
    std::vector<Utilization> utilizations;
    std::vector<char> satisfied;
    size_t depth = 0;
};

std::vector<Appointment> schedule (
    std::vector<Machine> &machines,
    std::vector<Demand> &demands,
    int day_length,
    const double reserve_ratio
)
{
    const double day_length_d = day_length;
    day_length = std::lround((double)day_length * (1 - reserve_ratio));
    
    std::vector<Appointment> appointments;

    int day = 0;

    std::vector<Frame> frames;
    Frame best_frame;
    size_t cycles = 0, best_cycles = 0;

    frames.emplace_back();
    frames.back().utilizations.resize(machines.size());
    frames.back().satisfied.resize(demands.size(), false);

    while (frames.size() > 0)
    {
        auto frame = frames.back();
        frames.pop_back();

        auto &utilizations = frame.utilizations;

        for (size_t j = 0; j < demands.size(); j++)
        {
            auto &demand = demands[j];

            for (size_t i = 0; i < machines.size(); i++)
            {
                auto &machine = machines[i];

                if (utilizations[i].total + demand.duration > day_length)
                {
                    continue;
                }

                if (demand.fractions == 0)
                {
                    continue;
                }

                if (frame.satisfied[j])
                {
                    continue;
                }

                if (std::find(
                    demand.machine_options.begin(),
                    demand.machine_options.end(),
                    machine.type
                ) == demand.machine_options.end())
                {
                    continue;
                }

                auto new_frame = frame;
                new_frame.depth++;

                new_frame.utilizations[i].total += demand.duration;
                new_frame.utilizations[i].reservations.push_back(&demand);
                new_frame.satisfied[j] = true;

                frames.emplace_back(std::move(new_frame));

                if (frames.back().depth > best_frame.depth)
                {
                    best_frame = frames.back();
                    best_cycles = cycles;
                    std::cerr << best_frame.depth << " " << cycles << std::endl;
                    if (best_frame.depth == demands.size())
                    {
                        std::cerr << "leaving" << std::endl;
                        goto done;
                    }
                }

                cycles++;
                if (best_frame.depth >= 5 && cycles > 10 * best_cycles && cycles > 3 * 1e6)
                {
                    // ending search cuz its leading nowhere
                    std::cerr << cycles << " " << best_cycles << std::endl;
                    goto done;
                }
            }
        }
    }

    done:
    for (size_t i = 0; i < machines.size(); i++)
    {
        auto &machine = machines[i];
        auto &utilization = best_frame.utilizations[i];

        const auto gap = (day_length_d - utilization.total) / utilization.reservations.size();

        double last_end = 0;
        for (size_t i = 0; i < utilization.reservations.size(); i++)
        {
            auto &demand = utilization.reservations[i];

            demand->fractions--;

            appointments.emplace_back(
                demand->id,
                machine.id,
                day,
                std::lround(last_end),
                demand->duration
            );

            last_end += demand->duration + gap;
        }
    }

    return appointments;
}

PYBIND11_MODULE(utils, m)
{
    py::class_<Machine>(m, "Machine")
        .def(
            py::init<const int, const std::string_view>(),
            py::arg("id"),
            py::arg("type")
        )
        .def_readwrite("id", &Machine::id)
        .def_readwrite("type", &Machine::type);

    py::class_<Demand>(m, "Demand")
        .def(py::init<
            const int, 
            const int, 
            const int,
            const bool, 
            const std::vector<std::string> &>(),
            py::arg("id"),
            py::arg("fractions"),
            py::arg("duration"),
            py::arg("is_inpatient"),
            py::arg("machine_options")
        )
        .def_readwrite("id", &Demand::id)
        .def_readwrite("fractions", &Demand::fractions)
        .def_readwrite("is_inpatient", &Demand::is_inpatient)
        .def_readwrite("machine_options", &Demand::machine_options);

    py::class_<Appointment>(m, "Appointment")
        .def(py::init<
            const int, 
            const int,
            const int,
            const int,
            const int>(),
            py::arg("demand_id"),
            py::arg("machine_id"),
            py::arg("day"),
            py::arg("start"),
            py::arg("duration")
        )
        .def_readwrite("demand_id", &Appointment::demand_id)
        .def_readwrite("machine_id", &Appointment::machine_id)
        .def_readwrite("day", &Appointment::day)
        .def_readwrite("start", &Appointment::start)
        .def_readwrite("duration", &Appointment::duration);

    m.def(
        "schedule", &schedule,
        py::arg("machines"),
        py::arg("demands"),
        py::arg("day_length"),
        py::arg("reserve_ratio")
    );
}
