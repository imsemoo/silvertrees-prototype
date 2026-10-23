"""Curated copy for the Silvertrees prototype.

Facts and wording come from silvertrees.net (research/catalog.json). Overrides here only clean
titles, add a one-line summary and a sector, and fill feature lists the old pages left empty.
"""

SECTORS = {
    "retail": "retail & e-commerce",
    "property": "property & building",
    "health": "health & professional",
    "media": "media & publishing",
    "food": "food & hospitality",
    "move": "motoring & logistics",
}

# order = order on the homepage of silvertrees.net
WORK = {
    "sold-expo": dict(title="Sold Expo", sector="property", line="An online trade show where 40+ real estate exhibitors meet their industry.",
                      kind="platform"),
    "psychmatters": dict(title="PSYCHmatters", sector="health", line="A Sydney psychology practice that books its own appointments.", kind="website"),
    "brydens-compensation-lawyers": dict(title="Brydens Compensation Lawyers", sector="health", line="A law firm's strong visual message, with the forms clients actually need.", kind="website"),
    "myflowermarket": dict(title="MyFlowerMarket", sector="retail", line="A marketplace that pays independent florists directly, searched by where the flowers are going.", kind="platform"),
    "global-knives": dict(title="Global Knives", sector="retail", line="A multi-layered responsive store for a famous Japanese knife brand.", kind="e-commerce"),
    "capstar": dict(title="Capstar", sector="retail", line="Caps shopped by brand, style and colour, turned 360° before you buy.", kind="e-commerce",
                    features=["360 degree image rotation", "Search by brand, style and colour", "Member registration for specials", "Gift cards and promotions"]),
    "trade-publishing-pty-ltd": dict(title="Trade Publishing", sector="media", line="A catalogue of current magazine issues and the advertising behind them.", kind="website"),
    "online-curtains": dict(title="Online Curtains", sector="retail", line="Made-to-measure curtains, configured step by step and priced on the spot.", kind="e-commerce",
                            features=["Save quotes to edit or buy later", "Styles, fabrics and tracks to choose from", "Secure payment", "A separate shop for fabrics, sliders and tracks", "Newsletter sign-up with regular specials"]),
    "classic-building": dict(title="Classic Building", sector="property", line="A premium home builder's gallery that prints its own brochures.", kind="website"),
    "sesmo": dict(title="SESMO", sector="health", line="Sydney East Podiatry, explained and bookable, on WordPress.", kind="website"),
    "portfolio-reel": dict(title="Portfolio & Reel", sector="media", line="A tiered subscription library of award-winning commercials going back to the 1980s.", kind="platform"),
    "doors-plus": dict(title="Doors Plus", sector="retail", line="No-fuss product search, catalogues and a store locator for every store in Australia.", kind="website",
                       features=["Store locator with directions", "Catalogues and downloads", "Online showrooms", "Product search across ranges"]),
    "viewmag": dict(title="ViewMag", sector="media", line="A Sydney lifestyle magazine you can read page by page, region by region.", kind="website"),
    "penthouse-on-bright-point": dict(title="Penthouse on Bright Point", sector="property", line="A holiday apartment on Magnetic Island that lets the views do the selling.", kind="website",
                                      features=["Dynamic booking system with live availability", "Virtual tour: video and slideshow", "Full-width background photography", "Owner-managed images, video and text"]),
    "mwt-foods": dict(title="MWT Foods", sector="food", line="Safe, healthy food information for clients, partners and supply chains.", kind="website"),
    "jayspjs": dict(title="JaysPJs", sector="retail", line="Pyjamas sold by size, with stock control the owner manages in-house.", kind="e-commerce"),
    "hardware-glass": dict(title="Hardware & Glass", sector="retail", line="Hundreds of keyword domains focused into one sales and enquiry engine.", kind="platform",
                           features=["Hundreds of keyword domains, each with unique content", "Instant stand-alone sites for associated companies", "Built-in sales and enquiry management", "Tiered sub-administration and central statistics"]),
    "scanpan": dict(title="Scanpan", sector="food", line="Every Scanpan range and product, plus recipes, guides and a consumer blog.", kind="website"),
    "nepean-motor-group": dict(title="Nepean Motor Group", sector="move", line="Vehicle search by lifestyle, brand and type, in a colour scheme you choose.", kind="website",
                               features=["Multi-level vehicle search", "Enquiries routed to the right staff member", "“Your Choice” colour picker for the whole site", "Fleet, employment and blog sections"]),
    "bhf-couriers": dict(title="BHF Couriers", sector="move", line="Instant courier quotes across Australia, with accounts and tracking.", kind="platform"),
    "di-lorenzo": dict(title="Di Lorenzo", sector="food", line="Brand and sales site for Di Lorenzo Caffe, built alongside its app.", kind="website"),
}

# features and titles cleaned of the "Features:" heading the old CMS leaked into titles
FIX_FEATURES = {
    "brydens-compensation-lawyers": ["Rotating full-page slideshow on the home page", "Customer enquiry forms", "Brochure and resource downloads", "Testimonials", "Office locator"],
    "scanpan": ["Extensive product listing", "Recipes", "Customer feedback and testimonials", "Competitions", "Consumer blog, care and user guides"],
}

PRODUCTS = {
    "online-expos": dict(title="Online Expos", line="The trade show, brought online: stands, live chat, presentations and e-commerce.", glyph="expo",
                         site="http://www.online-expos.com/"),
    "online-newsletters": dict(title="Online Newsletters", line="Build, send and print newsletters from your own dashboard, no HTML needed.", glyph="news",
                               site="http://www.online-newsletters.net/"),
    "online-organiser": dict(title="The Organiser", line="Contacts, reminders, links and notes, from any computer.", glyph="org", free=True,
                             site="http://www.onlineorganiser.net"),
    "help-desk-ticket-support-system": dict(title="Help Desk", line="Colour-coded support tickets with time tracking and a calendar of all open work.", glyph="desk",
                                            features=["Tiered administration and client roles", "Colour-coded status overview", "Assign, reassign or push back any ticket", "Time tracking per person and per job", "Full-screen calendar of ongoing work"]),
    "surveys-in-seconds": dict(title="Surveys in Seconds", line="Create. Review. Send. Insights. Feedback from your customers in four steps.", glyph="survey"),
    "filexchange": dict(title="FileXchange", line="Fast, secure file sharing that keeps your copyright and your files.", glyph="swap",
                        site="http://www.filexchange.com.au/"),
    "online-doc-store": dict(title="Online Doc Store", line="Your own document site and sub-domain, with a secure login for every client.", glyph="stack",
                             site="http://www.onlinedocstore.net/"),
    "e-therapy-com-au": dict(title="e-therapy", line="Secure online therapy sessions, booked with the therapist you choose.", glyph="talk",
                             site="http://www.e-therapy.com.au"),
}

NEWS = [
    dict(slug="online-newsletters", title="Online Newsletters", product="online-newsletters",
         line="The essential marketing tool for all your email and printing needs.",
         body=["Online Newsletters provides a unique email marketing system with a range of products designed to let you create and manage subscription lists, and create and send campaigns for high-resolution print and for the web, without expensive software or an expensive design studio.",
               "Manage and create professional newsletters online from your own user-friendly dashboard."]),
    dict(slug="the-silvertrees-organiser", title="The Silvertrees Organiser", product="online-organiser",
         line="Keep track of events, contacts, links and notes from any computer, anywhere. And it's free.",
         body=["One of the latest products to go live from the Silvertrees development team is the Organiser. We're very excited about what this simple yet highly efficient product can do.",
               "Setting up your organiser account only takes a few moments. Once set up you can start adding links, contacts, reminders and notes on the fly, so you stay on top of the important stuff. You can reach your data from any computer, anywhere, and even download a backup of all of it for offline viewing."]),
    dict(slug="the-business-expo", title="The Business Expo", product="online-expos",
         line="Over 200 Central Coast businesses, online and open all hours.",
         body=["Welcome to the Central Coast Online Business Expo. On display are over 200 of the very best Central Coast businesses across a wide variety of categories.",
               "No matter what you are looking for, the Central Coast Business Expo has something for you. It runs on Online Expos, the trade show system Silvertrees built and maintains."]),
]

HOSTING = {
    "intro": "Silvertrees provides a range of hosting packages tailored to your needs. Our secure servers sit in a state-of-the-art data centre in Alexandria, Sydney, with daily backups, technical support, and dedicated servers for anyone who needs large online storage.",
    "plans": [
        dict(name="standard", line="An affordable online presence.", items=["General multi-purpose site layouts", "Advertising and contact forms", "All-round admin with file and page content management"]),
        dict(name="business", line="Standard, plus a database behind it.", items=["Everything in standard", "Database access: subscription lists and resources", "E-commerce with online sales, order reports, invoices and products"], lead=True),
        dict(name="webmail", line="Included with hosting, or on its own.", items=["Up to 5 unique email accounts, many more aliases", "Add and delete users, monitor domains", "Shared files and calendars", "Forwarding and anti-spam filters"]),
    ],
}

COMPANY = dict(
    name="Silvertrees Web Development Pty Ltd",
    phone="+61 2 9063 8994", tel="+61290638994",
    email="gerard@silvertrees.net",
    support="helpdesk@thesitefactory.com.au",
    webmail="https://mail.silvertrees.net:7443/surgeweb",
    mailadmin="https://mail.silvertrees.net:7443/cgi/user.cgi",
    invoices="https://www.easyinvoices.com.au/",
    devs=6, designers=2,
)

# ---------- product presentation ----------
# grouped by the job each tool does; facts only from each product's own page
GROUPS = [
    ("sell and promote", "Reach customers and hear back from them.", ["online-expos", "online-newsletters", "surveys-in-seconds"]),
    ("run the office", "Keep work, people and dates in order.", ["help-desk-ticket-support-system", "online-organiser"]),
    ("share files securely", "Send and store documents without losing control of them.", ["filexchange", "online-doc-store"]),
    ("for practitioners", "A complete online service, ready to join.", ["e-therapy-com-au"]),
]

# which screen shows the product working (1-based index into its screenshots)
APP_SHOT = {"online-expos": 3, "online-newsletters": 4, "online-organiser": 1, "help-desk-ticket-support-system": 1,
            "surveys-in-seconds": 6, "filexchange": 4, "online-doc-store": 7, "e-therapy-com-au": 2}

STEPS = {
    "online-expos": [("set up", "Create the expo and its stands, each with its own branding, style and layout."),
                     ("present", "Exhibitors add profiles, multimedia presentations and products."),
                     ("meet", "Visitors browse 24/7, chat live with exhibitors and buy on the spot.")],
    "online-newsletters": [("build a list", "Create and manage your subscription lists."),
                           ("edit", "On-page instructions guide every change. No HTML needed."),
                           ("preview", "Send a preview to yourself with one click."),
                           ("send or print", "Email the campaign, or output it at high resolution for print.")],
    "surveys-in-seconds": [("create", "Choose a survey template or build your own."),
                           ("review", "Match it to your website or brand colours with style sheets."),
                           ("send", "Send and manage it from your account dashboard."),
                           ("insights", "Analyse the responses with the statistics component.")],
    "help-desk-ticket-support-system": [("log", "Tickets are categorised your way and colour-coded by status."),
                                        ("assign", "Give any ticket to anyone, reassign it, or push it back to the client."),
                                        ("track", "Every email, reply and attachment sits inline, with time logged per person.")],
    "online-organiser": [("sign up free", "Open an account in a few moments."),
                         ("add as you go", "Contacts, links, reminders and notes, from any computer."),
                         ("back up", "Download all of it for offline viewing whenever you like.")],
    "filexchange": [("upload", "Add documents to your secure dashboard."),
                    ("share", "Give clients their own login, or make items public for everyone."),
                    ("keep", "Files stay backed up and available 24/7, for as long as you want.")],
    "online-doc-store": [("get your site", "Your own website and sub-domain, like mysite.onlinedocstore.net."),
                         ("add clients", "Each client gets a secure login to upload and download."),
                         ("upload and notify", "Flag new files and the right people are told automatically.")],
    "e-therapy-com-au": [("choose", "Search for a therapist and view their details."),
                         ("register", "Sign up as a client in a few steps."),
                         ("book", "Book a secure online chat session from the calendar.")],
}

# where a product is already running on a Silvertrees client site
IN_USE = {
    "online-expos": [("Sold Expo", "work/sold-expo.html", "the online forum for real estate professionals"),
                     ("Central Coast Business Expo", "news/the-business-expo.html", "200+ Central Coast businesses")],
    "filexchange": [("Classic Building", "work/classic-building.html", "client files on a home builder's site")],
    "help-desk-ticket-support-system": [("Classic Building", "work/classic-building.html", "ticket login for clients")],
}

RELATED = {
    "online-expos": ["online-newsletters", "surveys-in-seconds"],
    "online-newsletters": ["surveys-in-seconds", "online-expos"],
    "surveys-in-seconds": ["online-newsletters", "help-desk-ticket-support-system"],
    "help-desk-ticket-support-system": ["filexchange", "online-organiser"],
    "online-organiser": ["help-desk-ticket-support-system", "online-newsletters"],
    "filexchange": ["online-doc-store", "help-desk-ticket-support-system"],
    "online-doc-store": ["filexchange", "help-desk-ticket-support-system"],
    "e-therapy-com-au": ["online-doc-store", "surveys-in-seconds"],
}

# FileXchange vs Online Doc Store, as each product describes itself
COMPARE = [
    ("what it is", "The light-weight version", "The full product, from a 2GB basic package"),
    ("where it lives", "Inside your existing website, or on its own", "Its own website and sub-domain"),
    ("client logins", "Yes", "Yes, each client uploads and downloads"),
    ("security", "Every security feature of Online Doc Store", "Secure client access to documents and files"),
    ("backups", "Backed up, available 24/7", "Daily, weekly and monthly offsite"),
]
