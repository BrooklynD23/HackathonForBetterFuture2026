import { useState } from "react";
import { Sparkles, Mail, MapPin, Calendar, Target } from "lucide-react";

const selectedOpportunity = {
  name: "AI & Machine Learning Hackathon",
  university: "USC",
  date: "March 28, 2026",
  location: "Los Angeles, CA",
  role: "Judge",
  tags: ["AI", "Machine Learning", "Innovation"],
  description:
    "A 24-hour hackathon focused on AI and ML solutions for social impact.",
};

const matchedVolunteers = [
  {
    id: 1,
    name: "Sarah Chen",
    role: "Senior Director",
    company: "Google",
    location: "Mountain View, CA",
    image: "SC",
    overallScore: 98,
    breakdown: {
      topicRelevance: 98,
      roleFit: 95,
      geoProximity: 92,
      availability: 100,
    },
    reasoning:
      "Sarah has extensive AI/ML expertise and has judged 5 similar hackathons in the past year. Her technical background and mentorship style align perfectly with this event.",
  },
  {
    id: 2,
    name: "David Kim",
    role: "Data Science Director",
    company: "Netflix",
    location: "Los Gatos, CA",
    image: "DK",
    overallScore: 95,
    breakdown: {
      topicRelevance: 96,
      roleFit: 92,
      geoProximity: 88,
      availability: 100,
    },
    reasoning:
      "David's data science and AI background make him an excellent fit. He has strong judging experience and is passionate about student engagement.",
  },
  {
    id: 3,
    name: "Emily Park",
    role: "Research Lead",
    company: "Stanford Research Institute",
    location: "Palo Alto, CA",
    image: "EP",
    overallScore: 92,
    breakdown: {
      topicRelevance: 94,
      roleFit: 88,
      geoProximity: 85,
      availability: 100,
    },
    reasoning:
      "Emily brings academic research expertise in ML and has a proven track record mentoring student competitions. Strong analytical skills for judging.",
  },
];

function ProgressBar({ value, color }: { value: number; color: string }) {
  return (
    <div className="w-full bg-gray-200 rounded-full h-2">
      <div
        className={`h-2 rounded-full ${color}`}
        style={{ width: `${value}%` }}
      />
    </div>
  );
}

export function AIMatching() {
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [selectedVolunteer, setSelectedVolunteer] = useState<number | null>(
    null
  );

  const volunteer = matchedVolunteers.find((v) => v.id === selectedVolunteer);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-3xl font-semibold text-gray-900">
            AI Matching Engine
          </h1>
        </div>
        <p className="text-gray-600">
          Intelligent volunteer-opportunity matching powered by AI
        </p>
      </div>

      {/* Selected Opportunity */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6 border border-purple-200">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              {selectedOpportunity.name}
            </h2>
            <p className="text-gray-700 mb-4">
              {selectedOpportunity.description}
            </p>
          </div>
          <span className="px-3 py-1 bg-purple-600 text-white text-sm rounded-full font-medium">
            Selected
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="flex items-center gap-2 text-sm">
            <Target className="w-4 h-4 text-purple-600" />
            <span className="text-gray-700">
              <span className="font-medium">University:</span>{" "}
              {selectedOpportunity.university}
            </span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Calendar className="w-4 h-4 text-purple-600" />
            <span className="text-gray-700">
              <span className="font-medium">Date:</span>{" "}
              {selectedOpportunity.date}
            </span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <MapPin className="w-4 h-4 text-purple-600" />
            <span className="text-gray-700">
              <span className="font-medium">Location:</span>{" "}
              {selectedOpportunity.location}
            </span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="text-gray-700">
              <span className="font-medium">Role:</span>{" "}
              {selectedOpportunity.role}
            </span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mt-4">
          {selectedOpportunity.tags.map((tag, index) => (
            <span
              key={index}
              className="px-3 py-1 bg-purple-600 text-white text-sm rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>

      {/* Top Matches */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              Top Recommended Volunteers
            </h2>
          </div>
          <span className="text-sm text-gray-600">
            Sorted by match score (highest first)
          </span>
        </div>

        <div className="space-y-6">
          {matchedVolunteers.map((vol) => (
            <div
              key={vol.id}
              className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex items-start gap-6 mb-6">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-400 to-blue-400 rounded-full flex items-center justify-center text-white text-2xl font-semibold flex-shrink-0">
                  {vol.image}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900">
                        {vol.name}
                      </h3>
                      <p className="text-gray-600">
                        {vol.role} at {vol.company}
                      </p>
                      <div className="flex items-center gap-2 text-sm text-gray-600 mt-1">
                        <MapPin className="w-4 h-4" />
                        {vol.location}
                      </div>
                    </div>
                    <div className="text-center flex-shrink-0">
                      <div className="w-20 h-20 rounded-full border-4 border-purple-600 flex items-center justify-center">
                        <div>
                          <p className="text-2xl font-bold text-purple-600">
                            {vol.overallScore}
                          </p>
                          <p className="text-xs text-gray-600">score</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-50 rounded-lg p-4 mb-4">
                    <p className="text-sm text-gray-700 italic">
                      {vol.reasoning}
                    </p>
                  </div>

                  {/* Match Breakdown */}
                  <div className="space-y-3">
                    <h4 className="font-medium text-gray-900">
                      Match Score Breakdown:
                    </h4>

                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-700">
                          Topic Relevance
                        </span>
                        <span className="text-sm font-medium text-gray-900">
                          {vol.breakdown.topicRelevance}%
                        </span>
                      </div>
                      <ProgressBar
                        value={vol.breakdown.topicRelevance}
                        color="bg-purple-600"
                      />
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-700">Role Fit</span>
                        <span className="text-sm font-medium text-gray-900">
                          {vol.breakdown.roleFit}%
                        </span>
                      </div>
                      <ProgressBar
                        value={vol.breakdown.roleFit}
                        color="bg-blue-600"
                      />
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-700">
                          Geographic Proximity
                        </span>
                        <span className="text-sm font-medium text-gray-900">
                          {vol.breakdown.geoProximity}%
                        </span>
                      </div>
                      <ProgressBar
                        value={vol.breakdown.geoProximity}
                        color="bg-green-600"
                      />
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-700">
                          Availability
                        </span>
                        <span className="text-sm font-medium text-gray-900">
                          {vol.breakdown.availability}%
                        </span>
                      </div>
                      <ProgressBar
                        value={vol.breakdown.availability}
                        color="bg-orange-600"
                      />
                    </div>
                  </div>

                  <button
                    onClick={() => {
                      setSelectedVolunteer(vol.id);
                      setShowEmailModal(true);
                    }}
                    className="mt-6 w-full px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium flex items-center justify-center gap-2"
                  >
                    <Mail className="w-5 h-5" />
                    Generate Outreach Email
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Email Generation Modal */}
      {showEmailModal && volunteer && (
        <div
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          onClick={() => setShowEmailModal(false)}
        >
          <div
            className="bg-white rounded-xl p-8 max-w-3xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Mail className="w-5 h-5 text-purple-600" />
                </div>
                <h2 className="text-2xl font-semibold text-gray-900">
                  AI-Generated Outreach Email
                </h2>
              </div>
              <button
                onClick={() => setShowEmailModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  To:
                </label>
                <input
                  type="text"
                  value={`${volunteer.name} <${volunteer.name.toLowerCase().replace(" ", ".")}@${volunteer.company.toLowerCase().replace(" ", "")}.com>`}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50"
                  readOnly
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Subject:
                </label>
                <input
                  type="text"
                  defaultValue={`Invitation: ${selectedOpportunity.name} at ${selectedOpportunity.university}`}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Message:
                </label>
                <textarea
                  rows={12}
                  defaultValue={`Dear ${volunteer.name},

I hope this message finds you well! I'm reaching out on behalf of the Insights Association West Chapter with an exciting opportunity that aligns perfectly with your expertise.

We've been invited to participate in the ${selectedOpportunity.name} at ${selectedOpportunity.university} on ${selectedOpportunity.date}, and we believe you would be an exceptional ${selectedOpportunity.role} for this event.

Given your extensive experience in ${volunteer.role} at ${volunteer.company} and your background in AI and machine learning, you would bring invaluable insights to the students participating in this hackathon. Your perspective would help shape the next generation of industry professionals.

Event Details:
• Date: ${selectedOpportunity.date}
• Location: ${selectedOpportunity.location}
• Role: ${selectedOpportunity.role}
• Duration: Approximately 4-6 hours

This is a fantastic opportunity to give back to the student community, strengthen IA's presence at ${selectedOpportunity.university}, and potentially identify future talent for our industry.

Would you be interested in participating? I'd be happy to provide more details and answer any questions you might have.

Thank you for considering this opportunity!

Best regards,
IA West Chapter Team`}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>

            <div className="flex items-center gap-3">
              <button className="flex-1 px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium">
                Send Email
              </button>
              <button className="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium">
                Save Draft
              </button>
              <button
                onClick={() => setShowEmailModal(false)}
                className="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
