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
    "jayspjs": dict(title="JaysPJs", sector="retail", line="Pyjamas sold by size, with stock control the owner runs herself.", kind="e-commerce"),
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
    "help-desk-ticket-support-system": dict(title="Help Desk", line="Colour-coded support tickets with time tracking and a calendar of everything in flight.", glyph="desk",
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
