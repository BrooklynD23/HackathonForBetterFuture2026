import { useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  CalendarDays,
  MapPin,
  Users,
  Building2,
} from "lucide-react";

const events = [
  {
    id: 1,
    title: "AI Hackathon",
    type: "university",
    date: "2026-03-28",
    university: "USC",
    location: "Los Angeles, CA",
    attendees: 150,
  },
  {
    id: 2,
    title: "IA Networking Mixer",
    type: "ia",
    date: "2026-03-30",
    location: "Downtown LA",
    attendees: 45,
  },
  {
    id: 3,
    title: "Career Fair",
    type: "university",
    date: "2026-04-05",
    university: "UCLA",
    location: "Los Angeles, CA",
    attendees: 300,
  },
  {
    id: 4,
    title: "IA Board Meeting",
    type: "ia",
    date: "2026-04-08",
    location: "Virtual",
    attendees: 12,
  },
  {
    id: 5,
    title: "Guest Lecture",
    type: "university",
    date: "2026-04-12",
    university: "Stanford",
    location: "Palo Alto, CA",
    attendees: 80,
  },
  {
    id: 6,
    title: "IA Spring Conference",
    type: "ia",
    date: "2026-04-15",
    location: "San Francisco, CA",
    attendees: 200,
  },
  {
    id: 7,
    title: "Data Competition",
    type: "university",
    date: "2026-04-18",
    university: "UC Berkeley",
    location: "Berkeley, CA",
    attendees: 120,
  },
  {
    id: 8,
    title: "Marketing Workshop",
    type: "university",
    date: "2026-04-22",
    university: "UCSD",
    location: "San Diego, CA",
    attendees: 60,
  },
  {
    id: 9,
    title: "IA Mentorship Kickoff",
    type: "ia",
    date: "2026-04-25",
    location: "Virtual",
    attendees: 50,
  },
  {
    id: 10,
    title: "Research Symposium",
    type: "university",
    date: "2026-05-03",
    university: "UC Irvine",
    location: "Irvine, CA",
    attendees: 100,
  },
];

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function getDaysInMonth(year: number, month: number) {
  return new Date(year, month + 1, 0).getDate();
}

function getFirstDayOfMonth(year: number, month: number) {
  return new Date(year, month, 1).getDay();
}

export function Calendar() {
  const [currentDate, setCurrentDate] = useState(new Date(2026, 2, 1)); // March 2026
  const [view, setView] = useState<"month" | "list">("month");
  const [filterType, setFilterType] = useState<"all" | "university" | "ia">("all");

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const daysInMonth = getDaysInMonth(year, month);
  const firstDay = getFirstDayOfMonth(year, month);

  const prevMonth = () => {
    setCurrentDate(new Date(year, month - 1, 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(year, month + 1, 1));
  };

  const getEventsForDate = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    return events.filter(
      (event) =>
        event.date === dateStr &&
        (filterType === "all" || event.type === filterType)
    );
  };

  const filteredEvents = events.filter(
    (event) => filterType === "all" || event.type === filterType
  );

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-semibold text-gray-900">Event Calendar</h1>
        <p className="text-gray-600 mt-1">
          Track university events and IA activities
        </p>
      </div>

      {/* Controls */}
      <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button
              onClick={prevMonth}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ChevronLeft className="w-5 h-5 text-gray-700" />
            </button>
            <h2 className="text-xl font-semibold text-gray-900 min-w-[200px] text-center">
              {months[month]} {year}
            </h2>
            <button
              onClick={nextMonth}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ChevronRight className="w-5 h-5 text-gray-700" />
            </button>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex gap-2">
              <button
                onClick={() => setView("month")}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  view === "month"
                    ? "bg-purple-600 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                Month
              </button>
              <button
                onClick={() => setView("list")}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  view === "list"
                    ? "bg-purple-600 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                List
              </button>
            </div>

            <select
              value={filterType}
              onChange={(e) =>
                setFilterType(e.target.value as "all" | "university" | "ia")
              }
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="all">All Events</option>
              <option value="university">University Events</option>
              <option value="ia">IA Events</option>
            </select>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap items-center gap-6 px-4">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-purple-500 rounded"></div>
          <span className="text-sm text-gray-700">University Events</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-blue-500 rounded"></div>
          <span className="text-sm text-gray-700">IA Events</span>
        </div>
      </div>

      {/* Calendar Views */}
      {view === "month" ? (
        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="grid grid-cols-7 gap-2">
            {/* Day headers */}
            {daysOfWeek.map((day) => (
              <div
                key={day}
                className="text-center text-sm font-medium text-gray-700 py-2"
              >
                {day}
              </div>
            ))}

            {/* Empty cells for days before month starts */}
            {Array.from({ length: firstDay }).map((_, index) => (
              <div key={`empty-${index}`} className="aspect-square"></div>
            ))}

            {/* Days of the month */}
            {Array.from({ length: daysInMonth }).map((_, index) => {
              const day = index + 1;
              const dayEvents = getEventsForDate(day);
              const isToday =
                day === 19 && month === 2 && year === 2026; // March 19, 2026

              return (
                <div
                  key={day}
                  className={`aspect-square border border-gray-200 rounded-lg p-2 ${
                    isToday ? "bg-purple-50 border-purple-300" : "bg-white"
                  }`}
                >
                  <div
                    className={`text-sm font-medium mb-1 ${
                      isToday ? "text-purple-600" : "text-gray-900"
                    }`}
                  >
                    {day}
                  </div>
                  <div className="space-y-1">
                    {dayEvents.slice(0, 2).map((event) => (
                      <div
                        key={event.id}
                        className={`text-xs p-1 rounded truncate ${
                          event.type === "university"
                            ? "bg-purple-100 text-purple-700"
                            : "bg-blue-100 text-blue-700"
                        }`}
                        title={event.title}
                      >
                        {event.title}
                      </div>
                    ))}
                    {dayEvents.length > 2 && (
                      <div className="text-xs text-gray-500">
                        +{dayEvents.length - 2} more
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredEvents.map((event) => (
            <div
              key={event.id}
              className={`bg-white rounded-xl p-6 border-l-4 border border-gray-200 shadow-sm hover:shadow-md transition-shadow ${
                event.type === "university"
                  ? "border-l-purple-500"
                  : "border-l-blue-500"
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {event.title}
                    </h3>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${
                        event.type === "university"
                          ? "bg-purple-100 text-purple-700"
                          : "bg-blue-100 text-blue-700"
                      }`}
                    >
                      {event.type === "university" ? "University" : "IA Event"}
                    </span>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <CalendarDays className="w-4 h-4" />
                      {new Date(event.date).toLocaleDateString("en-US", {
                        weekday: "long",
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                      })}
                    </div>
                    {event.university && (
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Building2 className="w-4 h-4" />
                        {event.university}
                      </div>
                    )}
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <MapPin className="w-4 h-4" />
                      {event.location}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Users className="w-4 h-4" />
                      ~{event.attendees} attendees
                    </div>
                  </div>
                </div>

                <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
