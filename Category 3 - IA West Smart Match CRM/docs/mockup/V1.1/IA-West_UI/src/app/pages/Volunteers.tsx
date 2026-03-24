import { useState } from "react";
import { Search, MapPin, Briefcase, Check, X } from "lucide-react";

const volunteers = [
  {
    id: 1,
    name: "Sarah Chen",
    role: "Senior Director",
    company: "Google",
    location: "Mountain View, CA",
    expertise: ["AI", "Machine Learning", "Product Strategy"],
    available: true,
    pastEngagements: 12,
    matchScoreAvg: 94,
    image: "SC",
  },
  {
    id: 2,
    name: "Michael Rodriguez",
    role: "VP of Marketing",
    company: "Adobe",
    location: "San Francisco, CA",
    expertise: ["Marketing", "Brand Strategy", "Digital"],
    available: true,
    pastEngagements: 18,
    matchScoreAvg: 91,
    image: "MR",
  },
  {
    id: 3,
    name: "Emily Park",
    role: "Research Lead",
    company: "Stanford Research Institute",
    location: "Palo Alto, CA",
    expertise: ["Research", "Analytics", "Academia"],
    available: false,
    pastEngagements: 8,
    matchScoreAvg: 96,
    image: "EP",
  },
  {
    id: 4,
    name: "David Kim",
    role: "Data Science Director",
    company: "Netflix",
    location: "Los Gatos, CA",
    expertise: ["Data Science", "Analytics", "AI"],
    available: true,
    pastEngagements: 15,
    matchScoreAvg: 92,
    image: "DK",
  },
  {
    id: 5,
    name: "Jessica Martinez",
    role: "Innovation Manager",
    company: "Meta",
    location: "Menlo Park, CA",
    expertise: ["Innovation", "Product", "Strategy"],
    available: true,
    pastEngagements: 10,
    matchScoreAvg: 89,
    image: "JM",
  },
  {
    id: 6,
    name: "Ryan Thompson",
    role: "Chief Analytics Officer",
    company: "Salesforce",
    location: "San Francisco, CA",
    expertise: ["Analytics", "Business Intelligence", "Leadership"],
    available: true,
    pastEngagements: 22,
    matchScoreAvg: 95,
    image: "RT",
  },
];

export function Volunteers() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedVolunteer, setSelectedVolunteer] = useState<number | null>(
    null
  );

  const filteredVolunteers = volunteers.filter(
    (vol) =>
      searchQuery === "" ||
      vol.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      vol.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
      vol.expertise.some((exp) =>
        exp.toLowerCase().includes(searchQuery.toLowerCase())
      )
  );

  const selectedVol = volunteers.find((v) => v.id === selectedVolunteer);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-semibold text-gray-900">
          Volunteer Profiles
        </h1>
        <p className="text-gray-600 mt-1">
          Browse and manage IA board member profiles
        </p>
      </div>

      {/* Search Bar */}
      <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search by name, company, or expertise..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>
      </div>

      {/* Volunteers Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {filteredVolunteers.map((volunteer) => (
          <div
            key={volunteer.id}
            className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => setSelectedVolunteer(volunteer.id)}
          >
            <div className="flex items-start gap-4 mb-4">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-blue-400 rounded-full flex items-center justify-center text-white text-xl font-semibold">
                {volunteer.image}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-gray-900 truncate">
                  {volunteer.name}
                </h3>
                <p className="text-sm text-gray-600">{volunteer.role}</p>
                <div className="flex items-center gap-2 mt-2">
                  {volunteer.available ? (
                    <span className="flex items-center gap-1 px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                      <Check className="w-3 h-3" />
                      Available
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 px-2 py-0.5 bg-red-100 text-red-700 text-xs rounded-full">
                      <X className="w-3 h-3" />
                      Unavailable
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="space-y-2 mb-4">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Briefcase className="w-4 h-4" />
                {volunteer.company}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <MapPin className="w-4 h-4" />
                {volunteer.location}
              </div>
            </div>

            <div className="mb-4">
              <p className="text-xs text-gray-500 mb-2">Expertise:</p>
              <div className="flex flex-wrap gap-1">
                {volunteer.expertise.map((exp, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-purple-50 text-purple-700 text-xs rounded-md"
                  >
                    {exp}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-gray-200">
              <div className="text-center">
                <p className="text-sm text-gray-600">Engagements</p>
                <p className="text-lg font-semibold text-gray-900">
                  {volunteer.pastEngagements}
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-600">Avg Score</p>
                <p className="text-lg font-semibold text-purple-600">
                  {volunteer.matchScoreAvg}%
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Detailed View Modal */}
      {selectedVol && (
        <div
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedVolunteer(null)}
        >
          <div
            className="bg-white rounded-xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start gap-6 mb-6">
              <div className="w-24 h-24 bg-gradient-to-br from-purple-400 to-blue-400 rounded-full flex items-center justify-center text-white text-3xl font-semibold">
                {selectedVol.image}
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-semibold text-gray-900">
                  {selectedVol.name}
                </h2>
                <p className="text-gray-600 mt-1">{selectedVol.role}</p>
                <p className="text-gray-600">{selectedVol.company}</p>
                <div className="flex items-center gap-2 mt-3">
                  {selectedVol.available ? (
                    <span className="flex items-center gap-1 px-3 py-1 bg-green-100 text-green-700 text-sm rounded-full">
                      <Check className="w-4 h-4" />
                      Available
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 px-3 py-1 bg-red-100 text-red-700 text-sm rounded-full">
                      <X className="w-4 h-4" />
                      Unavailable
                    </span>
                  )}
                </div>
              </div>
              <button
                onClick={() => setSelectedVolunteer(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="space-y-6">
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">
                  Contact Information
                </h3>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2 text-gray-600">
                    <MapPin className="w-4 h-4" />
                    {selectedVol.location}
                  </div>
                  <div className="flex items-center gap-2 text-gray-600">
                    <Briefcase className="w-4 h-4" />
                    {selectedVol.company}
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Expertise</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedVol.expertise.map((exp, index) => (
                    <span
                      key={index}
                      className="px-3 py-1.5 bg-purple-100 text-purple-700 text-sm rounded-lg"
                    >
                      {exp}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-3">
                  Engagement History
                </h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-gray-50 rounded-lg p-4 text-center">
                    <p className="text-2xl font-semibold text-gray-900">
                      {selectedVol.pastEngagements}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">
                      Total Engagements
                    </p>
                  </div>
                  <div className="bg-purple-50 rounded-lg p-4 text-center">
                    <p className="text-2xl font-semibold text-purple-600">
                      {selectedVol.matchScoreAvg}%
                    </p>
                    <p className="text-sm text-gray-600 mt-1">Avg Match Score</p>
                  </div>
                  <div className="bg-green-50 rounded-lg p-4 text-center">
                    <p className="text-2xl font-semibold text-green-600">
                      4.8
                    </p>
                    <p className="text-sm text-gray-600 mt-1">Rating</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-3">
                  Recent Engagements
                </h3>
                <div className="space-y-3">
                  {[
                    {
                      event: "USC AI Hackathon",
                      date: "Feb 15, 2026",
                      role: "Judge",
                    },
                    {
                      event: "UCLA Career Fair",
                      date: "Jan 28, 2026",
                      role: "Panelist",
                    },
                    {
                      event: "Stanford Workshop",
                      date: "Jan 12, 2026",
                      role: "Mentor",
                    },
                  ].map((engagement, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div>
                        <p className="font-medium text-gray-900">
                          {engagement.event}
                        </p>
                        <p className="text-sm text-gray-600">
                          {engagement.date}
                        </p>
                      </div>
                      <span className="px-3 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                        {engagement.role}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-3">
                  Preferred Roles
                </h3>
                <div className="flex flex-wrap gap-2">
                  {["Judge", "Mentor", "Speaker"].map((role, index) => (
                    <span
                      key={index}
                      className="px-3 py-1.5 bg-blue-100 text-blue-700 text-sm rounded-lg"
                    >
                      {role}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
