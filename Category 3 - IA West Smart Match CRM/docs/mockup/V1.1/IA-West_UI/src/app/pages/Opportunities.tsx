import { useState } from "react";
import {
  Search,
  Filter,
  MapPin,
  Calendar,
  Users,
  Sparkles,
  Building2,
} from "lucide-react";

const opportunities = [
  {
    id: 1,
    name: "AI & Machine Learning Hackathon",
    university: "USC",
    date: "March 28, 2026",
    location: "Los Angeles, CA",
    role: "Judge",
    tags: ["AI", "Machine Learning", "Innovation"],
    type: "Hackathon",
    participants: 150,
  },
  {
    id: 2,
    name: "Career Development Fair",
    university: "UCLA",
    date: "April 5, 2026",
    location: "Los Angeles, CA",
    role: "Panelist",
    tags: ["Career", "Marketing", "Industry"],
    type: "Career Fair",
    participants: 300,
  },
  {
    id: 3,
    name: "Guest Lecture: Market Research Trends",
    university: "Stanford University",
    date: "April 12, 2026",
    location: "Palo Alto, CA",
    role: "Speaker",
    tags: ["Research", "Analytics", "Trends"],
    type: "Guest Lecture",
    participants: 80,
  },
  {
    id: 4,
    name: "Data Analytics Competition",
    university: "UC Berkeley",
    date: "April 18, 2026",
    location: "Berkeley, CA",
    role: "Mentor",
    tags: ["Analytics", "Data Science", "Competition"],
    type: "Competition",
    participants: 120,
  },
  {
    id: 5,
    name: "Marketing Innovation Workshop",
    university: "UC San Diego",
    date: "April 22, 2026",
    location: "San Diego, CA",
    role: "Workshop Leader",
    tags: ["Marketing", "Innovation", "Strategy"],
    type: "Workshop",
    participants: 60,
  },
  {
    id: 6,
    name: "Research Methods Symposium",
    university: "UC Irvine",
    date: "May 3, 2026",
    location: "Irvine, CA",
    role: "Panelist",
    tags: ["Research", "Methods", "Academia"],
    type: "Symposium",
    participants: 100,
  },
];

const filters = {
  locations: ["All Locations", "Los Angeles", "San Francisco Bay Area", "San Diego", "Orange County"],
  roles: ["All Roles", "Judge", "Mentor", "Speaker", "Panelist", "Workshop Leader"],
  types: ["All Types", "Hackathon", "Career Fair", "Guest Lecture", "Competition", "Workshop", "Symposium"],
  tags: ["AI", "Marketing", "Research", "Analytics", "Data Science"],
};

export function Opportunities() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedLocation, setSelectedLocation] = useState("All Locations");
  const [selectedRole, setSelectedRole] = useState("All Roles");
  const [selectedType, setSelectedType] = useState("All Types");
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const filteredOpportunities = opportunities.filter((opp) => {
    const matchesSearch =
      searchQuery === "" ||
      opp.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      opp.university.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesLocation =
      selectedLocation === "All Locations" ||
      opp.location.includes(selectedLocation);
    const matchesRole = selectedRole === "All Roles" || opp.role === selectedRole;
    const matchesType = selectedType === "All Types" || opp.type === selectedType;
    const matchesTags =
      selectedTags.length === 0 ||
      selectedTags.some((tag) => opp.tags.includes(tag));

    return (
      matchesSearch && matchesLocation && matchesRole && matchesType && matchesTags
    );
  });

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold text-gray-900">
            Opportunities
          </h1>
          <p className="text-gray-600 mt-1">
            Discover and match university engagement opportunities
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
          <Sparkles className="w-5 h-5" />
          Find Best Matches
        </button>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm space-y-4">
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search opportunities by name or university..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        {/* Filter Row */}
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Filters:</span>
          </div>

          <select
            value={selectedLocation}
            onChange={(e) => setSelectedLocation(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
          >
            {filters.locations.map((loc) => (
              <option key={loc} value={loc}>
                {loc}
              </option>
            ))}
          </select>

          <select
            value={selectedRole}
            onChange={(e) => setSelectedRole(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
          >
            {filters.roles.map((role) => (
              <option key={role} value={role}>
                {role}
              </option>
            ))}
          </select>

          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
          >
            {filters.types.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        {/* Tag Filters */}
        <div className="flex flex-wrap gap-2">
          {filters.tags.map((tag) => (
            <button
              key={tag}
              onClick={() => toggleTag(tag)}
              className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                selectedTags.includes(tag)
                  ? "bg-purple-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      {/* Results Count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-600">
          Showing {filteredOpportunities.length} of {opportunities.length}{" "}
          opportunities
        </p>
      </div>

      {/* Opportunities Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredOpportunities.map((opportunity) => (
          <div
            key={opportunity.id}
            className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-2">
                  {opportunity.name}
                </h3>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Building2 className="w-4 h-4" />
                  {opportunity.university}
                </div>
              </div>
              <span className="px-3 py-1 bg-purple-100 text-purple-700 text-xs rounded-full font-medium">
                {opportunity.type}
              </span>
            </div>

            <div className="space-y-2 mb-4">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Calendar className="w-4 h-4" />
                {opportunity.date}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <MapPin className="w-4 h-4" />
                {opportunity.location}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Users className="w-4 h-4" />
                ~{opportunity.participants} participants
              </div>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">Required Role:</p>
              <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-sm rounded-lg font-medium">
                {opportunity.role}
              </span>
            </div>

            <div className="flex flex-wrap gap-2 mb-4">
              {opportunity.tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-md"
                >
                  {tag}
                </span>
              ))}
            </div>

            <button className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium flex items-center justify-center gap-2">
              <Sparkles className="w-4 h-4" />
              Find Best Match
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
