import re

with open("about.html", "r", encoding="utf-8") as f:
    about_html = f.read()

prefix = about_html.split("<main>")[0]
suffix = about_html.split("</main>")[1]

# Fix active navigation links
prefix = re.sub(r'class="nav-link nav-link-active\b[^"]*"', 'class="nav-link text-sm font-medium"', prefix)
prefix = prefix.replace('href="/Contactus" class="nav-link text-sm font-medium"', 'href="/Contactus" class="nav-link nav-link-active text-sm font-medium"')
prefix = prefix.replace('href="/Contactus" class="nav-link"', 'href="/Contactus" class="nav-link nav-link-active"')
prefix = prefix.replace('href="/Contactus">Contact Us</a>', 'href="/Contactus" style="color:#E87D2F;">Contact Us</a>')

# Change title
prefix = re.sub(r"<title>.*?</title>", "<title>Contact Us — SecureTech AV Designs</title>", prefix)

contact_specific_css = """
        .contact-hero {
            position: relative;
            background: url("{{ url_for('static', filename='contactus.png') }}") center/cover no-repeat;
            min-height: 50vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 0;
            padding-top: 80px;
        }
        .contact-hero::before {
            content: '';
            position: absolute;
            inset: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1;
        }
        .contact-hero h1 {
            color: #fff;
            font-size: clamp(2.5rem, 6vw, 4rem);
            font-weight: 800;
            position: relative;
            z-index: 2;
            text-transform: uppercase;
        }
        .contact-wrap {
            display: flex;
            gap: 80px;
            padding: 80px 1.5rem;
            align-items: flex-start;
            flex-wrap: wrap;
            justify-content: center;
            max-width: 1400px;
            margin: 0 auto;
        }
        @media(max-width:992px){.contact-wrap{flex-direction:column;gap:40px;padding:48px 16px}}

        .contact-info h2{font-size:clamp(1.8rem, 4vw, 2.5rem);font-weight:800;margin-bottom:8px;color:#0a1628;line-height:1.2;}
        .contact-info h2 .orange{color:#E87D2F}
        .contact-info .subtitle{color:#607080;font-size:1rem;line-height:1.7;margin-bottom:32px;max-width:440px}
        .contact-info h4{font-weight:700;color:#0a1628;margin-bottom:12px;text-transform:uppercase;letter-spacing:0.05em;}
        .contact-detail{display:flex;align-items:flex-start;gap:12px;margin-bottom:16px;font-size:0.95rem;color:#333;font-weight:500;}
        .contact-detail img{width:24px;margin-top:2px}

        .contact-form{background:#0a1628;color:#fff;padding:40px;border-radius:16px;min-width:400px;max-width:480px;box-shadow: 0 12px 40px rgba(10,22,40,0.15);}
        .contact-form h3{font-weight:700;font-size:1.5rem;margin-bottom:30px}
        .contact-form input,.contact-form textarea{width:100%;background:transparent;border:0;border-bottom:1px solid rgba(255,255,255,0.2);padding:12px 0;color:#fff;font-family:inherit;font-size:0.95rem;margin-bottom:20px;outline:0;transition:border-color 0.3s;}
        .contact-form input:focus,.contact-form textarea:focus{border-bottom-color:#E87D2F;}
        .contact-form input::placeholder,.contact-form textarea::placeholder{color:rgba(255,255,255,0.5)}
        .contact-form .flag-row{display:flex;align-items:center;gap:12px}
        .contact-form .flag-row img{width:36px;border-radius:4px;}
        .contact-form .flag-row input{flex:1}
        .contact-form textarea{height:100px;resize:vertical}
        .btn-submit{width:100%;padding:16px;background:#E87D2F;color:#fff;border:none;border-radius:8px;font-size:1rem;font-weight:600;cursor:pointer;transition:transform 0.3s, background 0.3s;margin-top:12px;display:flex;align-items:center;justify-content:center;gap:8px;}
        .btn-submit:hover{background:#d46f26;transform:translateY(-2px);}
        @media(max-width:768px){.contact-form{min-width:100%;width:100%;padding:30px 20px;}}

        .links-section{display:flex;gap:80px;padding:80px 1.5rem;align-items:flex-start;flex-wrap:wrap;justify-content:center;background:#f8fafc;}
        .links-box{background:#fff;padding:40px;border-radius:20px;box-shadow:0 8px 32px rgba(0,0,0,0.04);text-align:left;border:1px solid #e2e8f0;max-width:480px;}
        .links-box h2{font-weight:800;font-size:clamp(1.8rem, 4vw, 2.2rem);margin-bottom:8px;color:#0a1628;line-height:1.2;}
        .links-box .orange{color:#E87D2F}
        .links-box .info-row{display:flex;gap:16px;margin-top:24px;flex-wrap:wrap;}
        .links-box .info-row span{padding:12px 20px;border:1px solid #e2e8f0;border-radius:8px;font-size:0.95rem;font-weight:600;color:#0a1628;background:#f8fafc;}
        .quick-links h4{font-weight:700;margin-bottom:20px;color:#0a1628;text-transform:uppercase;letter-spacing:0.05em;font-size:0.9rem;}
        .quick-links a{display:block;color:#607080;margin-bottom:12px;font-size:0.95rem;transition:color 0.3s;font-weight:500;}
        .quick-links a:hover{color:#E87D2F}
        @media(max-width:768px){.links-section{flex-direction:column;gap:40px;padding:60px 16px}}
"""

prefix = prefix.replace("</style>", contact_specific_css + "\n    </style>")

contact_content = """
    <main>
        <div class="contact-hero fade-up">
            <h1>Contact Us</h1>
        </div>

        <div class="contact-wrap">
            <div class="contact-info fade-up" style="--delay:.1s">
                <h2>Get in Touch with</h2>
                <h2><span class="orange">Securetech AV Designs</span> 👋</h2>
                <p class="subtitle">Feel free to connect with us for any of your needs regarding our services. Our support team is ready to solve any of your issues. Just push a text and we will get back to you immediately.</p>
                <h4>INDIA</h4>
                <hr style="margin-bottom:24px;border:0;border-top:2px solid #1e1e1e;width:40px">
                <div class="contact-detail">
                    <img src="{{ url_for('static', filename='locator.png') }}" alt="Location">
                    <div>A-70-SECTOR 33 NOIDA, UTTAR PRADESH, 201301</div>
                </div>
                <div class="contact-detail">
                    <img src="{{ url_for('static', filename='message.png') }}" alt="Email">
                    <div>ashish@securetechav.com</div>
                </div>
                <div class="contact-detail">
                    <img src="{{ url_for('static', filename='phone.png') }}" alt="Phone">
                    <div>+91 7017247344</div>
                </div>
            </div>

            <form class="contact-form fade-up" id="contactForm" style="--delay:.2s">
                <h3>Drop Us A Message</h3>
                <input type="text" name="name" placeholder="Name*" required>
                <div class="flag-row">
                    <img src="{{ url_for('static', filename='flag.png') }}" alt="IN">
                    <input type="text" name="phone" placeholder="Phone No.*" required>
                </div>
                <input type="email" name="email" placeholder="Email*" required>
                <input type="text" name="company" placeholder="Company*" required>
                <input type="text" name="location" placeholder="Location*" required>
                <textarea name="message" placeholder="Message (Optional)"></textarea>
                <button type="submit" class="btn-submit">
                    Connect with Securetech today
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <path d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                </button>
            </form>
        </div>

        <div class="links-section">
            <div class="links-box fade-up">
                <h2>Get Ready to get</h2>
                <h2>Your <span class="orange">AV Solution</span></h2>
                <div class="info-row">
                    <span>info@securetechav.com</span>
                    <span>+91 7008166042</span>
                </div>
            </div>
            <div style="display:flex;gap:48px;flex-wrap:wrap" class="fade-up" style="--delay:.1s">
                <div class="quick-links">
                    <h4>Quick Links</h4>
                    <a href="/">Home</a>
                    <a href="/AboutUs">About Us</a>
                    <a href="/Solutionpage">Services</a>
                    <a href="https://drive.google.com/file/d/1VDGplc_6wfvQ7Y9-0vvbBtACm-72q_Cj/view" target="_blank">Corporate Profile</a>
                </div>
                <div class="quick-links">
                    <h4>Services</h4>
                    <a href="/Solutionpage">Audio Visual</a>
                    <a href="/Solutionpage">Architecture Acoustics</a>
                    <a href="/Solutionpage">Post project management</a>
                    <a href="/Solutionpage">Information Technology</a>
                </div>
            </div>
        </div>
    </main>
"""

final_html = prefix + contact_content + suffix

# Fix a small bug if link is unstyled in about
final_html = final_html.replace('href="/Contactus" class="nav-link text-sm font-medium"', 'href="/Contactus" class="nav-link nav-link-active text-sm font-medium"')

# make sure aboutus link loses active state
final_html = final_html.replace('href="/AboutUs" class="nav-link nav-link-active', 'href="/AboutUs" class="nav-link')


with open("contact.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Contact.html rewritten successfully")
