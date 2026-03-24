import { useState } from "react";
import {
  TrendingUp,
  ArrowRight,
  Filter,
  GraduationCap,
  CalendarDays,
  Users,
  UserPlus,
  Briefcase,
} from "lucide-react";
import {
  FunnelChart,
  Funnel,
  LabelList,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const pipelineData = [
  { stage: "Campus Engagement", count: 450, fill: "#a78bfa" },
  { stage: "IA Event", count: 320, fill: "#8b5cf6" },
  { stage: "Mentorship", count: 180, fill: "#7c3aed" },
  { stage: "Student Member", count: 95, fill: "#6d28d9" },
  { stage: "Professional Member", count: 42, fill: "#5b21b6" },
];

const conversionRates = [
  { from: "Engagement", to: "Event", rate: 71.1 },
  { from: "Event", to: "Mentorship", rate: 56.3 },
  { from: "Mentorship", to: "Student", rate: 52.8 },
  { from: "Student", to: "Professional", rate: 44.2 },
];

const universityBreakdown = [
  { name: "USC", engagement: 95, events: 72, mentorship: 42, student: 22, professional: 10 },
  { name: "UCLA", engagement: 88, events: 65, mentorship: 38, student: 19, professional: 9 },
  { name: "Stanford", engagement: 82, events: 58, mentorship: 35, student: 18, professional: 8 },
  { name: "Berkeley", engagement: 75, events: 52, mentorship: 28, student: 15, professional: 7 },
  { name: "UCSD", engagement: 65, events: 45, mentorship: 22, student: 12, professional: 5 },
  { name: "UCI", engagement: 45, events: 28, mentorship: 15, student: 9, professional: 3 },
];

const timeRanges = ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "All Time"];

export function Pipeline() {
  const [selectedTimeRange, setSelectedTimeRange] = useState("Last 6 Months");
  const [selectedUniversity, setSelectedUniversity] = useState("All Universities");

  const universities = ["All Universities", ...universityBreakdown.map(u => u.name)];

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-blue-500 rounded-lg flex items-center justify-center">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-3xl font-semibold text-gray-900">
            Pipeline Tracking
          </h1>
        </div>
        <p className="text-gray-600">
          Track student journey from campus engagement to professional membership
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Filters:</span>
          </div>

          <select
            value={selectedTimeRange}
            onChange={(e) => setSelectedTimeRange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
          >
            {timeRanges.map((range) => (
              <option key={range} value={range}>
                {range}
              </option>
            ))}
          </select>

          <select
            value={selectedUniversity}
            onChange={(e) => setSelectedUniversity(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
          >
            {universities.map((uni) => (
              <option key={uni} value={uni}>
                {uni}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <GraduationCap className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Campus Engaged</p>
              <p className="text-2xl font-semibold text-gray-900">450</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <CalendarDays className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Event Attendees</p>
              <p className="text-2xl font-semibold text-gray-900">320</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <Users className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">In Mentorship</p>
              <p className="text-2xl font-semibold text-gray-900">180</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
              <UserPlus className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Student Members</p>
              <p className="text-2xl font-semibold text-gray-900">95</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
              <Briefcase className="w-5 h-5 text-indigo-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Professional Members</p>
              <p className="text-2xl font-semibold text-gray-900">42</p>
            </div>
          </div>
        </div>
      </div>

      {/* Conversion Funnel */}
      <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">
          Conversion Funnel Overview
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <FunnelChart>
            <Tooltip />
            <Funnel dataKey="count" data={pipelineData} isAnimationActive>
              <LabelList
                position="right"
                fill="#000"
                stroke="none"
                dataKey="stage"
              />
            </Funnel>
          </FunnelChart>
        </ResponsiveContainer>
      </div>

      {/* Conversion Rates */}
      <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">
          Stage-to-Stage Conversion Rates
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {conversionRates.map((conversion, index) => (
            <div key={index} className="relative">
              <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl p-6 border border-purple-200">
                <div className="flex items-center justify-between mb-3">
                  <p className="text-sm text-gray-700 font-medium">
                    {conversion.from}
                  </p>
                  <ArrowRight className="w-5 h-5 text-purple-600" />
                  <p className="text-sm text-gray-700 font-medium">
                    {conversion.to}
                  </p>
                </div>
                <p className="text-3xl font-bold text-purple-600 text-center">
                  {conversion.rate}%
                </p>
                <p className="text-xs text-gray-600 text-center mt-1">
                  conversion rate
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* University Breakdown */}
      <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">
          Pipeline by University
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={universityBreakdown}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="engagement" fill="#a78bfa" name="Campus Engagement" />
            <Bar dataKey="events" fill="#8b5cf6" name="IA Events" />
            <Bar dataKey="mentorship" fill="#7c3aed" name="Mentorship" />
            <Bar dataKey="student" fill="#6d28d9" name="Student Members" />
            <Bar dataKey="professional" fill="#5b21b6" name="Professional Members" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Table */}
      <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">
          Detailed University Performance
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-700">
                  University
                </th>
                <th className="text-center py-3 px-4 text-sm font-medium text-gray-700">
                  Engagement
                </th>
                <th className="text-center py-3 px-4 text-sm font-medium text-gray-700">
                  Events
                </th>
                <th className="text-center py-3 px-4 text-sm font-medium text-gray-700">
                  Mentorship
                </th>
                <th className="text-center py-3 px-4 text-sm font-medium text-gray-700">
                  Student
                </th>
                <th className="text-center py-3 px-4 text-sm font-medium text-gray-700">
                  Professional
                </th>
                <th className="text-center py-3 px-4 text-sm font-medium text-gray-700">
                  Overall Rate
                </th>
              </tr>
            </thead>
            <tbody>
              {universityBreakdown.map((uni, index) => {
                const overallRate = ((uni.professional / uni.engagement) * 100).toFixed(1);
                return (
                  <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4">
                      <span className="font-medium text-gray-900">{uni.name}</span>
                    </td>
                    <td className="text-center py-4 px-4 text-gray-700">{uni.engagement}</td>
                    <td className="text-center py-4 px-4 text-gray-700">{uni.events}</td>
                    <td className="text-center py-4 px-4 text-gray-700">{uni.mentorship}</td>
                    <td className="text-center py-4 px-4 text-gray-700">{uni.student}</td>
                    <td className="text-center py-4 px-4 text-gray-700">{uni.professional}</td>
                    <td className="text-center py-4 px-4">
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                        {overallRate}%
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
