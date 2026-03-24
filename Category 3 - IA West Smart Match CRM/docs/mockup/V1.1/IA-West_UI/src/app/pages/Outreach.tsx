import { useState } from "react";
import {
  Mail,
  Send,
  Save,
  Edit,
  Plus,
  Sparkles,
  Building2,
  User,
} from "lucide-react";

const templates = [
  {
    id: 1,
    name: "Volunteer Invitation",
    category: "volunteer",
    subject: "Invitation: {{EVENT_NAME}} at {{UNIVERSITY}}",
    body: `Dear {{VOLUNTEER_NAME}},

I hope this message finds you well! I'm reaching out on behalf of the Insights Association West Chapter with an exciting opportunity that aligns perfectly with your expertise.

We've been invited to participate in the {{EVENT_NAME}} at {{UNIVERSITY}} on {{EVENT_DATE}}, and we believe you would be an exceptional {{ROLE}} for this event.

Event Details:
• Date: {{EVENT_DATE}}
• Location: {{LOCATION}}
• Role: {{ROLE}}
• Duration: {{DURATION}}

This is a fantastic opportunity to give back to the student community and strengthen IA's presence at {{UNIVERSITY}}.

Would you be interested in participating?

Best regards,
IA West Chapter Team`,
  },
  {
    id: 2,
    name: "University Partnership Proposal",
    category: "university",
    subject: "Partnership Opportunity: Insights Association West Chapter",
    body: `Dear {{CONTACT_NAME}},

My name is {{SENDER_NAME}}, and I'm reaching out on behalf of the Insights Association West Chapter. We're a professional organization dedicated to advancing the research and insights industry.

We would love to explore partnership opportunities with {{UNIVERSITY}} to:

• Provide industry speakers for guest lectures
• Offer mentorship for student projects and competitions
• Participate in career fairs and networking events
• Create internship and career pathways for students

Our members include senior professionals from companies like Google, Meta, Adobe, and Netflix, all passionate about supporting the next generation of industry talent.

Would you be available for a brief call to discuss potential collaboration?

Best regards,
{{SENDER_NAME}}
Insights Association West Chapter`,
  },
  {
    id: 3,
    name: "Event Follow-Up (Students)",
    category: "student",
    subject: "Thank You for Attending {{EVENT_NAME}}!",
    body: `Hi {{STUDENT_NAME}},

Thank you for attending {{EVENT_NAME}} on {{EVENT_DATE}}! It was wonderful meeting you and learning about your interests in {{TOPIC}}.

As a next step, I'd love to invite you to:

1. Join our mentorship program
2. Attend upcoming IA networking events
3. Explore student membership benefits

We're committed to supporting your career journey and would love to stay connected.

Feel free to reach out if you have any questions!

Best,
{{SENDER_NAME}}
Insights Association West Chapter`,
  },
  {
    id: 4,
    name: "Student Member Welcome",
    category: "student",
    subject: "Welcome to Insights Association!",
    body: `Dear {{STUDENT_NAME}},

Welcome to the Insights Association family! We're thrilled to have you as a student member.

As a member, you now have access to:

• Exclusive networking events
• Mentorship from industry professionals
• Career development resources
• Student-only workshops and webinars
• Job board and internship opportunities

Your Member ID: {{MEMBER_ID}}
Membership Portal: www.insightsassociation.org/student

We look forward to supporting your career journey!

Best regards,
IA West Chapter Team`,
  },
];

export function Outreach() {
  const [selectedTemplate, setSelectedTemplate] = useState(templates[0]);
  const [editMode, setEditMode] = useState(false);
  const [subject, setSubject] = useState(selectedTemplate.subject);
  const [body, setBody] = useState(selectedTemplate.body);
  const [showNewTemplate, setShowNewTemplate] = useState(false);

  const handleTemplateSelect = (template: typeof templates[0]) => {
    setSelectedTemplate(template);
    setSubject(template.subject);
    setBody(template.body);
    setEditMode(false);
  };

  const handleAIEnhance = () => {
    setBody(
      body +
        "\n\n[AI Enhanced: Added personalized industry insights and tailored call-to-action based on recipient profile]"
    );
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
            <Mail className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-3xl font-semibold text-gray-900">
            Outreach & Communications
          </h1>
        </div>
        <p className="text-gray-600">
          Manage email templates and communications
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Template Library */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-gray-900">Templates</h3>
              <button
                onClick={() => setShowNewTemplate(true)}
                className="p-2 bg-purple-100 text-purple-600 rounded-lg hover:bg-purple-200 transition-colors"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-2">
              {templates.map((template) => (
                <button
                  key={template.id}
                  onClick={() => handleTemplateSelect(template)}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    selectedTemplate.id === template.id
                      ? "bg-purple-50 border border-purple-200"
                      : "bg-gray-50 border border-transparent hover:bg-gray-100"
                  }`}
                >
                  <p className="font-medium text-gray-900 text-sm mb-1">
                    {template.name}
                  </p>
                  <div className="flex items-center gap-2">
                    {template.category === "volunteer" && (
                      <span className="flex items-center gap-1 px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full">
                        <User className="w-3 h-3" />
                        Volunteer
                      </span>
                    )}
                    {template.category === "university" && (
                      <span className="flex items-center gap-1 px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded-full">
                        <Building2 className="w-3 h-3" />
                        University
                      </span>
                    )}
                    {template.category === "student" && (
                      <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                        Student
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
            <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-2">
              <button className="w-full flex items-center gap-3 p-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors">
                <Sparkles className="w-5 h-5" />
                <span className="font-medium">AI Generate Email</span>
              </button>
              <button className="w-full flex items-center gap-3 p-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors">
                <Mail className="w-5 h-5" />
                <span className="font-medium">View Sent Emails</span>
              </button>
            </div>
          </div>
        </div>

        {/* Email Editor */}
        <div className="lg:col-span-2 bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-gray-900">
              {selectedTemplate.name}
            </h3>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setEditMode(!editMode)}
                className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                <Edit className="w-4 h-4" />
                {editMode ? "Preview" : "Edit"}
              </button>
            </div>
          </div>

          <div className="space-y-4">
            {/* Recipient */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                To:
              </label>
              <input
                type="text"
                placeholder="recipient@email.com"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>

            {/* Subject */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Subject:
              </label>
              {editMode ? (
                <input
                  type="text"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              ) : (
                <div className="px-4 py-2 bg-gray-50 rounded-lg text-gray-900">
                  {subject}
                </div>
              )}
            </div>

            {/* Body */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-sm font-medium text-gray-700">
                  Message:
                </label>
                {editMode && (
                  <button
                    onClick={handleAIEnhance}
                    className="flex items-center gap-1 text-sm text-purple-600 hover:text-purple-700"
                  >
                    <Sparkles className="w-4 h-4" />
                    AI Enhance
                  </button>
                )}
              </div>
              {editMode ? (
                <textarea
                  value={body}
                  onChange={(e) => setBody(e.target.value)}
                  rows={16}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 font-mono text-sm"
                />
              ) : (
                <div className="px-4 py-3 bg-gray-50 rounded-lg text-gray-900 whitespace-pre-wrap min-h-[400px]">
                  {body}
                </div>
              )}
            </div>

            {/* Variables Help */}
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <p className="text-sm font-medium text-blue-900 mb-2">
                Available Variables:
              </p>
              <div className="flex flex-wrap gap-2 text-xs">
                {[
                  "{{VOLUNTEER_NAME}}",
                  "{{EVENT_NAME}}",
                  "{{UNIVERSITY}}",
                  "{{EVENT_DATE}}",
                  "{{LOCATION}}",
                  "{{ROLE}}",
                  "{{DURATION}}",
                  "{{CONTACT_NAME}}",
                  "{{SENDER_NAME}}",
                  "{{STUDENT_NAME}}",
                  "{{TOPIC}}",
                  "{{MEMBER_ID}}",
                ].map((variable) => (
                  <code
                    key={variable}
                    className="px-2 py-1 bg-white text-blue-700 rounded border border-blue-300"
                  >
                    {variable}
                  </code>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-3 pt-4">
              <button className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium">
                <Send className="w-5 h-5" />
                Send Email
              </button>
              <button className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium flex items-center gap-2">
                <Save className="w-5 h-5" />
                Save Draft
              </button>
              <button className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium">
                Save as Template
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Emails */}
      <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Recent Emails
        </h3>
        <div className="space-y-3">
          {[
            {
              to: "Sarah Chen",
              subject: "Invitation: AI Hackathon at USC",
              date: "March 18, 2026",
              status: "Sent",
            },
            {
              to: "Dr. James Wilson",
              subject: "Partnership Opportunity: Insights Association",
              date: "March 17, 2026",
              status: "Opened",
            },
            {
              to: "Emily Park",
              subject: "Invitation: UCLA Career Fair",
              date: "March 16, 2026",
              status: "Replied",
            },
            {
              to: "Multiple Recipients (12)",
              subject: "Thank You for Attending Stanford Workshop",
              date: "March 15, 2026",
              status: "Sent",
            },
          ].map((email, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
            >
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-1">
                  <p className="font-medium text-gray-900">{email.to}</p>
                  <span
                    className={`px-2 py-0.5 text-xs rounded-full ${
                      email.status === "Sent"
                        ? "bg-blue-100 text-blue-700"
                        : email.status === "Opened"
                          ? "bg-purple-100 text-purple-700"
                          : "bg-green-100 text-green-700"
                    }`}
                  >
                    {email.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{email.subject}</p>
              </div>
              <p className="text-sm text-gray-500">{email.date}</p>
            </div>
          ))}
        </div>
      </div>

      {/* New Template Modal */}
      {showNewTemplate && (
        <div
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          onClick={() => setShowNewTemplate(false)}
        >
          <div
            className="bg-white rounded-xl p-8 max-w-2xl w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">
              Create New Template
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Template Name:
                </label>
                <input
                  type="text"
                  placeholder="e.g., Event Confirmation"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category:
                </label>
                <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500">
                  <option>Volunteer</option>
                  <option>University</option>
                  <option>Student</option>
                </select>
              </div>
              <div className="flex gap-3 pt-4">
                <button className="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium">
                  Create Template
                </button>
                <button
                  onClick={() => setShowNewTemplate(false)}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
