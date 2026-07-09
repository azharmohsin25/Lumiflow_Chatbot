APP_NAME = "LumiFlow"
TAGLINE = "A polished FAQ assistant that answers product questions with intent-aware matching."
SUBTITLE = (
    "Clean the text, compare it with curated FAQs, and serve the closest answer with a fallback "
    "that stays helpful instead of guessing."
)

FEATURES = [
    {
        "title": "Text cleanup",
        "detail": "Lowercase, tokenize, remove stop words, and normalize word forms before matching.",
    },
    {
        "title": "Intent-aware ranking",
        "detail": "Cosine similarity over question variants captures how people actually phrase support questions.",
    },
    {
        "title": "Confidence fallback",
        "detail": "When a query is vague, the bot shows the nearest FAQs so users can keep moving.",
    },
]

STARTER_PROMPTS = [
    "What is LumiFlow and who is it for?",
    "How do I reset my password?",
    "Can I invite teammates and assign roles?",
    "Does LumiFlow integrate with Slack?",
]

FAQS = [
    {
        "category": "Product",
        "intent": "product-overview",
        "question": "What is LumiFlow and who is it for?",
        "answer": (
            "LumiFlow is a simple workflow and support hub for small teams that want cleaner "
            "communication, better task visibility, and faster customer answers. It is a great fit "
            "for startups, service businesses, and product teams that need one place to organize work."
        ),
        "tags": ["what is lumiflow", "overview", "who is it for", "product demo", "about the app"],
        "phrases": [
            "tell me about LumiFlow",
            "what does LumiFlow do",
            "who should use LumiFlow",
            "give me a product overview",
        ],
    },
    {
        "category": "Account",
        "intent": "password-reset",
        "question": "How do I reset my password?",
        "answer": (
            "From the sign-in screen, choose Forgot password, enter the email on your account, and "
            "follow the reset link we send you. If the email does not arrive, check spam and make "
            "sure the address matches your LumiFlow login."
        ),
        "tags": ["password", "reset", "sign in", "forgot login", "account access"],
        "phrases": [
            "I forgot my password",
            "can't log in",
            "need to reset my login",
            "password help",
        ],
    },
    {
        "category": "Team",
        "intent": "invite-team",
        "question": "Can I invite teammates and assign roles?",
        "answer": (
            "Yes. Open Team Settings, add your coworkers by email, and pick a role for each person. "
            "Owners can manage billing and permissions, admins can manage the workspace, and members "
            "can handle day-to-day work."
        ),
        "tags": ["invite teammates", "roles", "permissions", "team members", "workspace access"],
        "phrases": [
            "how do I add a coworker",
            "invite people to my workspace",
            "set user roles",
            "who can manage permissions",
        ],
    },
    {
        "category": "Billing",
        "intent": "upgrade-plan",
        "question": "How do I change or upgrade my plan?",
        "answer": (
            "Go to Billing, choose Manage plan, and pick the plan you want. Changes happen right away "
            "and the updated rate is reflected on the next invoice. You can upgrade or downgrade at any time."
        ),
        "tags": ["upgrade plan", "change subscription", "billing", "pricing", "plan change"],
        "phrases": [
            "switch my subscription",
            "change plans",
            "update billing tier",
            "move to a bigger plan",
        ],
    },
    {
        "category": "Billing",
        "intent": "payment-methods",
        "question": "What payment methods are accepted?",
        "answer": (
            "We accept major credit cards and debit cards. Annual plans can also be paid by invoice for "
            "approved accounts. If your company needs a custom billing setup, contact support and we will help."
        ),
        "tags": ["payment methods", "credit card", "invoice", "billing", "card"],
        "phrases": [
            "how can I pay",
            "what cards do you accept",
            "can I pay by invoice",
            "billing payment options",
        ],
    },
    {
        "category": "Billing",
        "intent": "invoices",
        "question": "Can I download invoices or receipts?",
        "answer": (
            "Yes. Open Billing > Documents to view and download every invoice or receipt in PDF format. "
            "If you need a tax-friendly copy or company details updated, support can regenerate the document."
        ),
        "tags": ["invoice", "receipt", "billing documents", "pdf", "download receipt"],
        "phrases": [
            "where are my invoices",
            "download my receipt",
            "billing documents",
            "get a PDF invoice",
        ],
    },
    {
        "category": "Analytics",
        "intent": "export-reports",
        "question": "How do I export reports?",
        "answer": (
            "Open the Reports page, choose the date range you need, and click Export. You can export "
            "data as CSV for spreadsheets or PDF for sharing with stakeholders."
        ),
        "tags": ["export reports", "csv", "pdf", "analytics", "download data"],
        "phrases": [
            "download analytics",
            "save report as csv",
            "export data",
            "can I print the report",
        ],
    },
    {
        "category": "Integrations",
        "intent": "integrations",
        "question": "Does LumiFlow integrate with Slack, Google Calendar, or Zapier?",
        "answer": (
            "Yes. LumiFlow connects with Slack for notifications, Google Calendar for scheduling, and "
            "Zapier for custom automations. If you need a different integration, the API can bridge most workflows."
        ),
        "tags": ["integrations", "slack", "google calendar", "zapier", "api"],
        "phrases": [
            "connect to Slack",
            "sync with Google Calendar",
            "set up Zapier",
            "does it have integrations",
        ],
    },
    {
        "category": "Security",
        "intent": "security",
        "question": "Is my data secure?",
        "answer": (
            "Your data is encrypted in transit and at rest, access is permission-based, and backups are "
            "run automatically. We also support two-factor authentication to keep accounts protected."
        ),
        "tags": ["security", "encrypted", "data protection", "two-factor", "backup"],
        "phrases": [
            "how secure is my data",
            "is the app encrypted",
            "do you support 2fa",
            "what protects my account",
        ],
    },
    {
        "category": "Billing",
        "intent": "cancel-plan",
        "question": "How do I cancel my subscription?",
        "answer": (
            "Go to Billing > Plan, choose Cancel subscription, and follow the confirmation steps. "
            "Your workspace stays active until the end of the current billing period, so you do not lose access immediately."
        ),
        "tags": ["cancel subscription", "end plan", "billing", "stop renewal", "downgrade"],
        "phrases": [
            "how do I stop renewal",
            "cancel my plan",
            "end my subscription",
            "leave the paid plan",
        ],
    },
    {
        "category": "Product",
        "intent": "mobile-app",
        "question": "Is there a mobile app?",
        "answer": (
            "LumiFlow is fully mobile responsive in the browser, and the companion app is available on "
            "iOS and Android for teams that want quick access on the go."
        ),
        "tags": ["mobile app", "ios", "android", "responsive", "on the go"],
        "phrases": [
            "do you have an app",
            "can I use this on my phone",
            "is there an iPhone app",
            "mobile access",
        ],
    },
    {
        "category": "Account",
        "intent": "delete-account",
        "question": "Can I delete my account and data?",
        "answer": (
            "Yes. Open Account Settings and choose Delete account. The workspace owner can remove the "
            "workspace, and we keep a short retention window only for legal or billing obligations."
        ),
        "tags": ["delete account", "remove data", "privacy", "account settings", "workspace delete"],
        "phrases": [
            "erase my data",
            "close my account",
            "remove my profile",
            "delete workspace",
        ],
    },
    {
        "category": "Support",
        "intent": "support",
        "question": "What support options are available?",
        "answer": (
            "You can reach support by email, in-app chat, or the help center. Standard plans get a response "
            "within one business day, while higher tiers receive faster priority support."
        ),
        "tags": ["support", "help center", "contact", "response time", "chat"],
        "phrases": [
            "how do I contact support",
            "where is the help center",
            "what are your support hours",
            "how fast do you reply",
        ],
    },
    {
        "category": "Trial",
        "intent": "free-trial",
        "question": "Do you offer a free trial?",
        "answer": (
            "Yes. New teams can start with a free 14-day trial that includes the core workflow, reporting, "
            "and integration features. No credit card is required until you are ready to upgrade."
        ),
        "tags": ["free trial", "trial", "start for free", "no credit card", "trial period"],
        "phrases": [
            "can I try it for free",
            "how long is the trial",
            "do I need a card to start",
            "test the product first",
        ],
    },
]
