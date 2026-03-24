import { MetricCard } from "../components/MetricCard";
import {
  Briefcase,
  Users,
  CalendarDays,
  TrendingUp,
  Sparkles,
  ArrowRight,
} from "lucide-react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  FunnelChart,
  Funnel,
  LabelList,
} from "recharts";

const funnelData = [
  { name: "Campus Engagement", value: 450, fill: "#a78bfa" },
  { name: "IA Event Attendance", value: 320, fill: "#8b5cf6" },
  { name: "Mentorship Program", value: 180, fill: "#7c3aed" },
  { name: "Student Member", value: 95, fill: "#6d28d9" },
  { name: "Professional Member", value: 42, fill: "#5b21b6" },
];

const weeklyMatches = [
  { day: "Mon", matches: 12 },
  { day: "Tue", matches: 18 },
  { day: "Wed", matches: 15 },
  { day: "Thu", matches: 22 },
  { day: "Fri", matches: 19 },
  { day: "Sat", matches: 8 },
  { day: "Sun", matches: 5 },
];

const monthlyTrend = [
  { month: "Sep", opportunities: 28, volunteers: 45 },
  { month: "Oct", opportunities: 35, volunteers: 48 },
  { month: "Nov", opportunities: 42, volunteers: 52 },
  { month: "Dec", opportunities: 38, volunteers: 50 },
  { month: "Jan", opportunities: 48, volunteers: 55 },
  { month: "Feb", opportunities: 52, volunteers: 58 },
];

const topMatches = [
  {
    volunteer: "Sarah Chen",
    opportunity: "USC AI Hackathon - Judge",
    score: 98,
    role: "AI/ML Expert",
  },
  {
    volunteer: "Michael Rodriguez",
    opportunity: "UCLA Career Fair - Panelist",
    score: 96,
    role: "Industry Leader",
  },
  {
    volunteer: "Emily Park",
    opportunity: "Stanford Guest Lecture - Speaker",
    score: 94,
    role: "Research Specialist",
  },
  {
    volunteer: "David Kim",
    opportunity: "Berkeley Data Challenge - Mentor",
    score: 92,
    role: "Analytics Pro",
  },
];

export function Dashboard() {
  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-semibold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">
          Welcome back! Here's your university engagement overview.
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Active Opportunities"
          value={52}
          change="+12% from last month"
          changeType="positive"
          icon={Briefcase}
          iconColor="bg-blue-100 text-blue-600"
        />
        <MetricCard
          title="Volunteer Utilization"
          value="84%"
          change="+5% from last month"
          changeType="positive"
          icon={Users}
          iconColor="bg-green-100 text-green-600"
        />
        <MetricCard
          title="Upcoming Events"
          value={18}
          change="Next 30 days"
          changeType="neutral"
          icon={CalendarDays}
          iconColor="bg-purple-100 text-purple-600"
        />
        <MetricCard
          title="Conversion Rate"
          value="9.3%"
          change="+2.1% improvement"
          changeType="positive"
          icon={TrendingUp}
          iconColor="bg-orange-100 text-orange-600"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Conversion Funnel */}
        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">
            Conversion Funnel
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <FunnelChart>
              <Tooltip />
              <Funnel dataKey="value" data={funnelData} isAnimationActive>
                <LabelList
                  position="right"
                  fill="#000"
                  stroke="none"
                  dataKey="name"
                />
              </Funnel>
            </FunnelChart>
          </ResponsiveContainer>
        </div>

        {/* Weekly Match Activity */}
        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">
            Weekly AI Matches
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weeklyMatches}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="matches" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Monthly Trends */}
      <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
        <h3 className="font-semibold text-gray-900 mb-4">
          6-Month Activity Trend
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={monthlyTrend}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="opportunities"
              stroke="#8b5cf6"
              strokeWidth={3}
              name="Opportunities"
            />
            <Line
              type="monotone"
              dataKey="volunteers"
              stroke="#3b82f6"
              strokeWidth={3}
              name="Active Volunteers"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Top Matches This Week */}
      <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-600" />
            <h3 className="font-semibold text-gray-900">
              Top AI Matches This Week
            </h3>
          </div>
          <button className="text-sm text-purple-600 hover:text-purple-700 font-medium flex items-center gap-1">
            View All
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        <div className="space-y-4">
          {topMatches.map((match, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border border-purple-100 hover:shadow-md transition-shadow"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <p className="font-semibold text-gray-900">
                    {match.volunteer}
                  </p>
                  <span className="px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded-full">
                    {match.role}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  {match.opportunity}
                </p>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <p className="text-sm text-gray-600">Match Score</p>
                  <p className="text-2xl font-semibold text-purple-600">
                    {match.score}%
                  </p>
                </div>
                <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium">
                  Connect
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
