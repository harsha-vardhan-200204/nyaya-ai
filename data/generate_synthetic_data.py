import os
import pandas as pd
import random
from datetime import datetime, timedelta

# Create directories
os.makedirs("H:/intern/project/nyaya-ai/data/demo", exist_ok=True)

# 1. GENERATE LEGAL SECTIONS
sections_data = []

# Standard Indian Acts
acts_list = [
    {"name": "Indian Contract Act", "year": 1872, "domain": "Contract Law", "url": "https://www.indiacode.nic.in/handle/123456789/2187"},
    {"name": "Information Technology Act", "year": 2000, "domain": "Cyber Law", "url": "https://www.indiacode.nic.in/handle/123456789/1999"},
    {"name": "Negotiable Instruments Act", "year": 1881, "domain": "Cheque/payment disputes", "url": "https://www.indiacode.nic.in/handle/123456789/2189"},
    {"name": "Consumer Protection Act", "year": 2019, "domain": "Consumer Law", "url": "https://www.indiacode.nic.in/handle/123456789/11100"},
    {"name": "Transfer of Property Act", "year": 1882, "domain": "Property Law", "url": "https://www.indiacode.nic.in/handle/123456789/2334"},
    {"name": "Indian Penal Code", "year": 1860, "domain": "Criminal Law", "url": "https://www.indiacode.nic.in/handle/123456789/2265"},
    {"name": "Code of Criminal Procedure", "year": 1973, "domain": "Criminal Law", "url": "https://www.indiacode.nic.in/handle/123456789/1612"},
    {"name": "Protection of Women from Domestic Violence Act", "year": 2005, "domain": "Family Law", "url": "https://www.indiacode.nic.in/handle/123456789/2021"}
]

# Section details
sections_templates = [
    # Indian Contract Act
    {"act": "Indian Contract Act", "section": "10", "title": "What agreements are contracts", 
     "desc": "All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void.", 
     "keywords": "agreement, contract, consent, competency, consideration, lawful"},
    {"act": "Indian Contract Act", "section": "73", "title": "Compensation for loss or damage caused by breach of contract", 
     "desc": "When a contract has been broken, the party who suffers by such breach is entitled to receive, from the party who has broken the contract, compensation for any loss or damage caused to him thereby, which naturally arose in the usual course of things from such breach, or which the parties knew, when they made the contract, to be likely to result from the breach of it.", 
     "keywords": "compensation, breach, damages, loss, contract, agreement"},
    {"act": "Indian Contract Act", "section": "74", "title": "Compensation for breach of contract where penalty stipulated for", 
     "desc": "When a contract has been broken, if a sum is named in the contract as the amount to be paid in case of such breach, or if the contract contains any other stipulation by way of penalty, the party complaining of the breach is entitled, whether or not actual damage or loss is proved to have been incurred, to receive from the party who has broken the contract reasonable compensation not exceeding the amount so named or, as the case may be, the penalty stipulated for.", 
     "keywords": "liquidated damages, penalty, breach, contract, compensation"},
    
    # IT Act
    {"act": "Information Technology Act", "section": "43", "title": "Penalty and compensation for damage to computer, computer system, etc.", 
     "desc": "If any person without permission of the owner or any other person who is incharge of a computer, computer system or computer network accesses, downloads, copies, introduces virus, damages, disrupts, denies access, or facilitates access, he shall be liable to pay damages by way of compensation to the person so affected.", 
     "keywords": "access, hacking, damage, computer, virus, compensation, penalty"},
    {"act": "Information Technology Act", "section": "66", "title": "Computer related offences", 
     "desc": "If any person, dishonestly or fraudulently, does any act referred to in section 43, he shall be punishable with imprisonment for a term which may extend to three years or with fine which may extend to five lakh rupees or with both.", 
     "keywords": "computer offence, criminal hacker, fraud, theft"},
    {"act": "Information Technology Act", "section": "66C", "title": "Punishment for identity theft", 
     "desc": "Whoever, fraudulently or dishonestly, make use of the electronic signature, password or any other unique identification feature of any other person, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to rupees one lakh.", 
     "keywords": "identity theft, password, cloning, spoofing, fraud, electronic signature"},
    {"act": "Information Technology Act", "section": "66D", "title": "Punishment for cheating by personation by using computer resource", 
     "desc": "Whoever, by means of any communication device or computer resource cheats by personating, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to one lakh rupees.", 
     "keywords": "cheating, personation, online scam, phishing, fraud, cybercrime"},

    # NI Act
    {"act": "Negotiable Instruments Act", "section": "138", "title": "Dishonour of cheque for insufficiency, etc., of funds in the account", 
     "desc": "Where any cheque drawn by a person on an account maintained by him with a banker for payment of any amount of money to another person from out of that account for the discharge, in whole or in part, of any debt or other liability, is returned by the bank unpaid, either because of the amount of money standing to the credit of that account is insufficient to honour the cheque or that it exceeds the amount arranged to be paid from that account, such person shall be deemed to have committed an offence and shall be punished with imprisonment for a term which may extend to two years, or with fine which may extend to twice the amount of the cheque, or with both.", 
     "keywords": "cheque bounce, dishonour, insufficient funds, signature mismatch, cheque, payment dispute"},
    {"act": "Negotiable Instruments Act", "section": "139", "title": "Presumption in favour of holder", 
     "desc": "It shall be presumed, unless the contrary is proved, that the holder of a cheque received the cheque of the nature referred to in section 138 for the discharge, in whole or in part, of any debt or other liability.", 
     "keywords": "presumption, holder, burden of proof, cheque, debt"},
    
    # Consumer Protection Act
    {"act": "Consumer Protection Act", "section": "2(11)", "title": "Deficiency in Service", 
     "desc": "Deficiency means any fault, imperfection, shortcoming or inadequacy in the quality, nature and manner of performance which is required to be maintained by or under any law for the time being in force or has been undertaken to be performed by a person in pursuance of a contract or otherwise in relation to any service.", 
     "keywords": "deficiency, service, negligence, delay, consumer dispute"},
    {"act": "Consumer Protection Act", "section": "35", "title": "Manner in which complaint shall be made", 
     "desc": "A complaint, in relation to any goods sold or delivered or agreed to be sold or delivered or any service provided or agreed to be provided, may be filed with a District Commission by the consumer or any recognized consumer association.", 
     "keywords": "consumer complaint, district commission, filing, consumer"},

    # Transfer of Property Act
    {"act": "Transfer of Property Act", "section": "54", "title": "Sale defined, Sale how made", 
     "desc": "Sale is a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised. Such transfer, in the case of tangible immoveable property of the value of one hundred rupees and upwards can be made only by a registered instrument.", 
     "keywords": "sale, property, registration, deed, ownership transfer, sale agreement"},
    {"act": "Transfer of Property Act", "section": "105", "title": "Lease defined", 
     "desc": "A lease of immoveable property is a transfer of a right to enjoy such property, made for a certain time, express or implied, or in perpetuity, in consideration of a price paid or promised, or of money, a share of crops, service or any other thing of value, to be rendered periodically or on specified occasions to the transferor by the transferee, who accepts the transfer on such terms.", 
     "keywords": "lease, tenant, landlord, rent, rent agreement, lease deed"},
    {"act": "Transfer of Property Act", "section": "108", "title": "Rights and liabilities of lessor and lessee", 
     "desc": "Defines the rights and obligations of both the landlord (lessor) and the tenant (lessee), including the obligation to return the property in good condition, the right to recover security deposits, and rules regarding damage and repairs.", 
     "keywords": "landlord duties, tenant rights, security deposit, maintenance, repairs, damage"},

    # IPC
    {"act": "Indian Penal Code", "section": "300", "title": "Murder", 
     "desc": "Except in the cases hereinafter excepted, culpable homicide is murder, if the act by which the death is caused is done with the intention of causing death, or with the intention of causing bodily injury as the offender knows to be likely to cause death, or is sufficient in the ordinary course of nature to cause death.", 
     "keywords": "murder, homicide, killing, intention, bodily injury"},
    {"act": "Indian Penal Code", "section": "302", "title": "Punishment for murder", 
     "desc": "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.", 
     "keywords": "punishment, murder, death penalty, life imprisonment"},
    {"act": "Indian Penal Code", "section": "378", "title": "Theft", 
     "desc": "Whoever, intending to take dishonestly any moveable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft.", 
     "keywords": "theft, stealing, moveable property, consent, dishonest intention"},
    {"act": "Indian Penal Code", "section": "379", "title": "Punishment for theft", 
     "desc": "Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.", 
     "keywords": "theft, punishment, stealing, jail"},
    {"act": "Indian Penal Code", "section": "420", "title": "Cheating and dishonestly inducing delivery of property", 
     "desc": "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.", 
     "keywords": "cheating, fraud, forgery, inducement, financial fraud, property delivery"},

    # DV Act / CrPC Family
    {"act": "Protection of Women from Domestic Violence Act", "section": "12", "title": "Application to Magistrate", 
     "desc": "An aggrieved person or a Protection Officer or any other person on behalf of the aggrieved person may present an application to the Magistrate seeking one or more reliefs under this Act, including protection order, residence order, monetary relief, custody order, or compensation order.", 
     "keywords": "domestic violence, magistrate application, maintenance, protection order, physical abuse"},
    {"act": "Code of Criminal Procedure", "section": "125", "title": "Order for maintenance of wives, children and parents", 
     "desc": "If any person having sufficient means neglects or refuses to maintain his wife, unable to maintain herself, or his legitimate or illegitimate minor child, a Magistrate of the first class may, upon proof of such neglect or refusal, order such person to make a monthly allowance for the maintenance of his wife or child.", 
     "keywords": "maintenance, alimony, support, wife, children, magistrate, divorce"}
]

# Expand to 100 synthetic sections by creating variants and other sections
all_sections = []
sec_id = 1
for s_temp in sections_templates:
    act_meta = next(a for a in acts_list if a["name"] == s_temp["act"])
    all_sections.append({
        "act_id": sec_id,
        "act_name": s_temp["act"],
        "year": act_meta["year"],
        "section": s_temp["section"],
        "title": s_temp["title"],
        "description": s_temp["desc"],
        "keywords": s_temp["keywords"],
        "domain": act_meta["domain"],
        "source_url": act_meta["url"] + f"/section_{s_temp['section']}",
        "active_status": "Active"
    })
    sec_id += 1

# Generate remaining synthetic sections up to 105 to hit 100+ target
extra_sections = [
    ("Indian Contract Act", "11", "Who are competent to contract", "Minors and persons of unsound mind are not competent.", "minor, competency, contract"),
    ("Indian Contract Act", "23", "What considerations and objects are lawful, and what not", "Consideration or object must not be unlawful, fraudulent, or against public policy.", "unlawful consideration, public policy, void agreement"),
    ("Indian Contract Act", "39", "Effect of refusal of party to perform promise wholly", "When a party refuses, the promisee may put an end to the contract.", "breach, refusal, termination"),
    ("Information Technology Act", "43A", "Compensation for failure to protect data", "Body corporate failing to protect sensitive personal data is liable to pay damages.", "data privacy, security, breach, data leak, compensation"),
    ("Information Technology Act", "66E", "Punishment for violation of privacy", "Intentionally capturing, publishing images of private areas without consent.", "privacy, camera, voyeurism, cyber crime"),
    ("Information Technology Act", "67", "Punishment for publishing obscene material in electronic form", "Publishing or transmitting obscene material in electronic form is punishable.", "obscene, cyber crime, explicit content"),
    ("Negotiable Instruments Act", "140", "Defence which may not be allowed in any prosecution under section 138", "It shall not be a defence in a prosecution that the drawer had no reason to believe that the cheque may be dishonoured.", "defence, cheque, drawer, trial"),
    ("Negotiable Instruments Act", "141", "Offences by companies", "If the person committing an offence under section 138 is a company, every person in charge is liable.", "company check, director liability, corporate cheque"),
    ("Consumer Protection Act", "2(1) (g)", "Defect in goods", "Any fault, imperfection or shortcoming in the quality, quantity, potency, purity or standard of goods.", "defect, product, consumer, poor quality"),
    ("Consumer Protection Act", "84", "Liability of product manufacturer", "Product manufacturer shall be liable in a product liability action if product contains manufacturing defect.", "product liability, manufacturing defect, personal injury"),
    ("Transfer of Property Act", "53A", "Part performance", "Where any person contracts to transfer for consideration any immoveable property and the transferee has taken possession.", "part performance, possession, contract"),
    ("Transfer of Property Act", "106", "Duration of certain leases in absence of written contract", "Lease of immoveable property for agricultural or manufacturing purposes shall be deemed to be from year to year.", "lease duration, termination notice, eviction"),
    ("Transfer of Property Act", "111", "Determination of lease", "A lease of immoveable property determines by efflux of time, forfeiture, surrender, or notice to quit.", "lease termination, expiry, forfeiture, eviction"),
    ("Indian Penal Code", "323", "Punishment for voluntarily causing hurt", "Punishment for voluntarily causing hurt is imprisonment up to one year or fine up to 1000 rupees.", "hurt, assault, simple injury, violence"),
    ("Indian Penal Code", "325", "Punishment for voluntarily causing grievous hurt", "Punishment for grievous hurt is imprisonment up to seven years and fine.", "grievous hurt, fracture, severe injury, bone break"),
    ("Indian Penal Code", "341", "Punishment for wrongful restraint", "Punishment for preventing any person from proceeding in any direction.", "wrongful restraint, block, illegal confinement"),
    ("Indian Penal Code", "379", "Punishment for theft", "Whoever commits theft shall be punished with imprisonment up to 3 years.", "theft, steal, punishment"),
    ("Indian Penal Code", "406", "Punishment for criminal breach of trust", "Whoever commits criminal breach of trust shall be punished with imprisonment up to 3 years.", "breach of trust, misappropriation, security deposit, fraud"),
    ("Indian Penal Code", "506", "Punishment for criminal intimidation", "Whoever commits the offence of criminal intimidation shall be punished with imprisonment up to 2 years.", "threat, intimidation, blackmail, extortion"),
    ("Code of Criminal Procedure", "437", "When bail may be taken in case of non-bailable offence", "Provisions for bail when a person accused of non-bailable offence is arrested without warrant.", "bail, non-bailable, magistrate, release"),
    ("Code of Criminal Procedure", "438", "Direction for grant of bail to person apprehending arrest", "Anticipatory bail applications filed before High Court or Court of Session.", "anticipatory bail, arrest apprehension, police custody"),
    ("Code of Criminal Procedure", "482", "Saving of inherent powers of High Court", "High Court has inherent powers to prevent abuse of process of court or to secure ends of justice.", "quash, inherent power, FIR quashing, high court"),
    ("Protection of Women from Domestic Violence Act", "18", "Protection orders", "Magistrate may pass a protection order prohibiting the respondent from committing domestic violence.", "protection order, abuse, stay order, domestic violence"),
    ("Protection of Women from Domestic Violence Act", "19", "Residence orders", "Magistrate may pass a residence order restraining the respondent from dispossessing the wife from shared household.", "residence order, shared household, eviction, wife support"),
    ("Protection of Women from Domestic Violence Act", "20", "Monetary reliefs", "Magistrate may direct the respondent to pay monetary relief to meet the expenses incurred by wife.", "monetary relief, medical expenses, loss of earnings, maintenance")
]

# Fill the rest with synthetic variants to reach 105 sections
for act_name, sec_num, title, desc, kw in extra_sections:
    act_meta = next(a for a in acts_list if a["name"] == act_name)
    all_sections.append({
        "act_id": sec_id,
        "act_name": act_name,
        "year": act_meta["year"],
        "section": sec_num,
        "title": title,
        "description": desc,
        "keywords": kw,
        "domain": act_meta["domain"],
        "source_url": act_meta["url"] + f"/section_{sec_num}",
        "active_status": "Active"
    })
    sec_id += 1

# Generate synthetic sections for remaining domains like Cyber, Banking, Labour to total 110 sections
remaining_domains = ["Cyber Law", "Banking Law", "Consumer Law", "Criminal Law", "Property Law"]
for i in range(110 - len(all_sections)):
    dom = random.choice(remaining_domains)
    act_name = "Synthetic Act on " + dom
    sec_num = str(random.randint(1, 150))
    all_sections.append({
        "act_id": sec_id,
        "act_name": act_name,
        "year": random.randint(1980, 2024),
        "section": sec_num,
        "title": f"Provisions regarding {dom} violation",
        "description": f"This section details the penalty and civil liability associated with violations of {dom} regulations under Indian law.",
        "keywords": f"synthetic, {dom.lower()}, provision, penalty, liability",
        "domain": dom,
        "source_url": f"https://www.indiacode.nic.in/synthetic_{sec_id}",
        "active_status": "Active"
    })
    sec_id += 1

df_sections = pd.DataFrame(all_sections)
df_sections.to_csv("H:/intern/project/nyaya-ai/data/demo/legal_sections.csv", index=False)
print("Generated", len(df_sections), "sections.")


# 2. GENERATE LEGAL CASES (120 records)
cases_data = []

# Setup core categories and their specific parameters for similarity / outcome / counterfactual simulation.
# Note: we add factual indicators like:
# 'written_contract', 'notice_sent', 'receipt_exists', 'evidence_present'
# inside the text, so our ML model can parse them or use simple NLP features for outcome prediction.

category_scenarios = {
    "Landlord/Tenant disputes": {
        "acts": "Transfer of Property Act",
        "sections": "108;105",
        "keywords": "landlord, tenant, security deposit, rent, damage, eviction, lease deed",
        "court": ["District Court Bangalore", "Civil Court Delhi", "Small Causes Court Mumbai", "High Court of Karnataka"],
        "states": ["Karnataka", "Delhi", "Maharashtra", "Tamil Nadu"],
        "facts_templates": [
            "The petitioner is a tenant who leased the premises from the respondent (landlord) under a written agreement dated {date}. The tenant vacated the property on {vacate_date} after serving a 1-month notice. However, the landlord refused to refund the security deposit of Rs. {amount}, alleging minor wear-and-tear damages to the walls. The tenant claims no structural damage occurred.",
            "The tenant had been residing in the property under an oral agreement since {date}. Upon vacating, the landlord locked the premises and withheld the deposit of Rs. {amount} without any justification or damage report. The tenant had paid all electricity and water bills and possesses water-tight payment receipts.",
            "A landlord filed a suit for eviction of a tenant who stopped paying monthly rent of Rs. {rent} since {date}. The landlord sent a legal notice under Section 106 of the Transfer of Property Act, but the tenant did not vacate. The tenant claims the landlord refused to execute necessary repairs making the flat inhabitable."
        ],
        "allowed_outcome": {
            "outcome": "Allowed",
            "judgment": "The court held that under Section 108 of the Transfer of Property Act, the landlord is bound to return the security deposit upon peaceful handover of possession, subject only to reasonable deductions for actual damages. Since the landlord failed to provide receipts of repair or proof of structural damage, the entire deposit must be refunded with 6% interest.",
            "evidence": "Written rent agreement, Bank statements showing deposit payment, Notice to vacate, Photos of vacated premises showing clean condition.",
            "arguments": "Petitioner argued security deposit withholding is illegal under the lease terms. Respondent argued structural alterations were done by tenant which required expensive restoration."
        },
        "dismissed_outcome": {
            "outcome": "Dismissed",
            "judgment": "The court found that the tenant did not serve the mandatory notice of termination before vacating. Furthermore, the landlord submitted structural assessment and invoices proving the tenant caused major damage to the bathroom plumbing and electrical systems, the cost of which exceeded the security deposit amount. Withholding of deposit is justified.",
            "evidence": "Invoices of repairs, Surveyor report of structural damage, Leaked water bills unpaid by tenant.",
            "arguments": "Petitioner claimed damages were regular wear and tear. Respondent presented invoices of plumbing repairs and structural surveyor report."
        }
    },
    "Cheque/payment disputes": {
        "acts": "Negotiable Instruments Act",
        "sections": "138;139",
        "keywords": "cheque bounce, dishonour, insufficient funds, signature mismatch, notice, liability",
        "court": ["Metropolitan Magistrate Mumbai", "Chief Judicial Magistrate Pune", "Judicial Magistrate Chennai", "High Court of Delhi"],
        "states": ["Maharashtra", "Tamil Nadu", "Delhi", "Karnataka"],
        "facts_templates": [
            "The complainant supplied goods to the accused, who issued a cheque for Rs. {amount} dated {date} in discharge of the outstanding liability. Upon presentation, the cheque was returned dishonoured with the remarks 'Funds Insufficient'. The complainant sent a statutory legal notice within 30 days, but the accused failed to pay.",
            "The complainant lent a friendly loan of Rs. {amount} to the accused in cash. The accused issued a post-dated cheque which bounced due to 'Signature Mismatch'. Complainant issued legal notice. The accused claims the cheque was given for security purposes and no loan was actually taken.",
            "The accused issued a cheque of Rs. {amount} to clear a business invoice. The cheque bounced with remark 'Account Closed'. A legal notice was sent via speed post and delivered on {notice_date}, but the accused did not respond nor pay the amount within 15 days."
        ],
        "allowed_outcome": {
            "outcome": "Convicted",
            "judgment": "The court held that under Section 139 of the Negotiable Instruments Act, there is a statutory presumption in favour of the holder of the cheque that it was issued for the discharge of a legally enforceable debt. The accused failed to lead any cogent evidence to rebut this presumption. The accused is convicted under Section 138 NI Act.",
            "evidence": "Original dishonoured cheque, Bank return memo, Office copy of statutory legal notice, Speed post delivery receipt, Business invoice.",
            "arguments": "Complainant argued the debt is legally enforceable through invoices. Accused argued the cheque was stolen and signature was forged."
        },
        "dismissed_outcome": {
            "outcome": "Acquitted",
            "judgment": "The court observed that the complainant failed to prove that the statutory legal notice was served on the accused within the mandatory 30-day window from the bank return memo date. As the service of notice is a condition precedent to attract Section 138, the complaint is dismissed and the accused is acquitted.",
            "evidence": "Postal tracking report showing delay/non-delivery of notice, Bank returns date log.",
            "arguments": "Complainant argued notice was sent to last known address. Accused argued they changed address and no notice was received within 30 days."
        }
    },
    "Cybercrime": {
        "acts": "Information Technology Act;Indian Penal Code",
        "sections": "66D;420",
        "keywords": "online fraud, phishing, impersonation, credit card, bank transaction, cyber fraud, fake identity",
        "court": ["Chief Metropolitan Magistrate Delhi", "Cyber Crime Court Bangalore", "Sessions Court Hyderabad"],
        "states": ["Delhi", "Karnataka", "Telangana", "Maharashtra"],
        "facts_templates": [
            "The victim received a phone call from an unknown person impersonating a bank manager. The caller induced the victim to share an OTP for card verification. Consequently, Rs. {amount} was fraudulently debited from the victim's account and transferred to a digital wallet. The police traced the wallet to the accused.",
            "The accused created a fake website resembling a popular e-commerce platform and induced multiple customers to pay online for discounted electronics. Customers did not receive any goods. Cyber police registered an FIR under Section 66D of the IT Act and Section 420 of the IPC.",
            "The accused hacked into the complainant's email account, spoofed their business email address, and instructed a client to deposit an invoice payment of Rs. {amount} into a fraudulent bank account controlled by the accused."
        ],
        "allowed_outcome": {
            "outcome": "Convicted",
            "judgment": "The court found that the prosecution successfully proved the digital audit trail. The IP addresses, bank account logs, and mobile phone IMEI data conclusively linked the accused to the phishing website and unauthorized transaction. The accused is convicted under Section 66D IT Act and 420 IPC.",
            "evidence": "IP address logs, Bank transaction statements, Phone records, Forensic report of seized laptop, OTP SMS logs.",
            "arguments": "Prosecution argued digital evidence clearly identifies the accused. Defence argued the accused's Wi-Fi was hacked and someone else used their IP address."
        },
        "dismissed_outcome": {
            "outcome": "Acquitted",
            "judgment": "The court held that the digital evidence submitted by the cyber cell lacked the mandatory certification under Section 65B of the Indian Evidence Act. Without a valid electronic record certificate, the IP logs and hard drive copies are inadmissible. The accused is acquitted due to lack of admissible evidence.",
            "evidence": "Digital logs lacking 65B certificate, Seized phone with no data logs.",
            "arguments": "Prosecution argued digital logs show clear connections. Defence argued no certificate under 65B was submitted, rendering files inadmissible."
        }
    },
    "Contract Law": {
        "acts": "Indian Contract Act",
        "sections": "73;10",
        "keywords": "breach of contract, specific performance, commercial dispute, damages, agreement, non-payment",
        "court": ["High Court of Karnataka", "Delhi High Court", "City Civil Court Chennai"],
        "states": ["Karnataka", "Delhi", "Tamil Nadu"],
        "facts_templates": [
            "The plaintiff entered into a supply agreement with the defendant for delivering raw materials worth Rs. {amount}. The plaintiff paid an advance of Rs. {advance}. The defendant failed to deliver the materials within the agreed timeline, causing a complete shutdown of the plaintiff's factory. The plaintiff claims damages for loss of business.",
            "A service agreement was signed between a software development firm and a client. The client stopped payments midway, claiming the software had major bugs. The development firm sued the client for the unpaid invoices of Rs. {amount}, presenting email communications indicating client satisfaction and sign-offs.",
            "The buyer paid a deposit of Rs. {amount} for buying machinery. The seller refused to deliver the machinery and sold it to a third party at a higher price. The buyer files a suit for recovery of deposit and breach of contract damages."
        ],
        "allowed_outcome": {
            "outcome": "Allowed",
            "judgment": "The court observed that the defendant committed a clear breach by failing to perform their contractual obligation within the stipulated time. Under Section 73 of the Contract Act, the plaintiff is entitled to recover the advance and receive reasonable damages that naturally arose from the breach.",
            "evidence": "Written agreement, Email correspondence, Bank transactions, Production loss ledger, Invoices.",
            "arguments": "Plaintiff argued the delay directly halted factory output. Defendant argued force majeure due to transport strike."
        },
        "dismissed_outcome": {
            "outcome": "Dismissed",
            "judgment": "The court found that there was no concluded contract between the parties, as the emails exchanged were merely negotiations and no formal agreement was executed (lacking Section 10 parameters). Additionally, the plaintiff did not suffer any quantifiable loss. The suit is dismissed.",
            "evidence": "Negotiation drafts, Vague email replies, No financial books proving actual losses.",
            "arguments": "Plaintiff claimed informal emails form a contract. Defendant argued no final offer and acceptance took place."
        }
    },
    "Family Law": {
        "acts": "Code of Criminal Procedure;Protection of Women from Domestic Violence Act",
        "sections": "125;12",
        "keywords": "maintenance, domestic violence, wife support, alimony, child custody, physical abuse",
        "court": ["Family Court Bangalore", "Family Court Noida", "Sessions Court Mumbai"],
        "states": ["Karnataka", "Uttar Pradesh", "Maharashtra"],
        "facts_templates": [
            "The petitioner wife filed for maintenance under Section 125 CrPC, stating she was driven out of the matrimonial home by the husband and is unable to maintain herself. She claims the husband earns Rs. {income} per month as a software engineer and refuses to support her. The husband claims she left voluntarily.",
            "The applicant filed a petition under Section 12 of the Domestic Violence Act alleging continuous physical abuse and emotional torture by the husband and in-laws. She sought a protection order, residence order, and monthly maintenance of Rs. {maintenance}.",
            "A petition for maintenance was filed by the wife on behalf of herself and her minor child. She submitted school fee invoices and medical bills. The husband argues he has been laid off and has zero income."
        ],
        "allowed_outcome": {
            "outcome": "Allowed",
            "judgment": "The court observed that the husband has a social and legal duty to maintain his wife and minor child. The husband's claim of unemployment cannot absolve him of his duty to maintain. He is ordered to pay monthly maintenance of Rs. {maintenance} to the wife.",
            "evidence": "Marriage certificate, Income tax returns of husband, Child's school fee receipt, Medical certificates showing treatment of domestic abuse.",
            "arguments": "Wife argued she has no source of income and resides in parents' house. Husband argued wife is highly qualified and can work."
        },
        "dismissed_outcome": {
            "outcome": "Dismissed",
            "judgment": "The court found that the wife is highly qualified, runs a successful boutique business, and generates substantial income. Since she left the matrimonial home without any reasonable cause and refuses to return despite the husband's petition for restitution of conjugal rights, her claim for maintenance is dismissed.",
            "evidence": "GST registration and bank statement of wife's business, Photos showing wife running business, Decree of restitution of conjugal rights.",
            "arguments": "Wife argued boutique is running in loss. Husband presented bank records showing boutique's high turnover."
        }
    }
}

# Generate 125 cases
case_id = 1001
scenarios_keys = list(category_scenarios.keys())

for i in range(125):
    # Pick a category
    cat = random.choice(scenarios_keys)
    scen = category_scenarios[cat]
    
    # Determine outcome
    is_allowed = random.choice([True, False])
    outcome_meta = scen["allowed_outcome"] if is_allowed else scen["dismissed_outcome"]
    
    # Format facts
    date_val = (datetime.now() - timedelta(days=random.randint(300, 1000))).strftime("%Y-%m-%d")
    vacate_val = (datetime.now() - timedelta(days=random.randint(30, 299))).strftime("%Y-%m-%d")
    notice_val = (datetime.now() - timedelta(days=random.randint(200, 250))).strftime("%Y-%m-%d")
    amt_val = random.choice([50000, 100000, 250000, 500000, 1500000])
    advance_val = random.choice([10000, 25000, 50000])
    rent_val = random.choice([15000, 25000, 45000])
    inc_val = random.choice([80000, 120000, 200000])
    maint_val = random.choice([10000, 20000, 35000])
    
    fact_text = random.choice(scen["facts_templates"]).format(
        date=date_val, vacate_date=vacate_val, amount=amt_val, rent=rent_val, notice_date=notice_val, income=inc_val, maintenance=maint_val, advance=advance_val
    )
    
    # Party naming
    first_names = ["Ramesh", "Suresh", "Amit", "Rajesh", "Vikram", "Sunita", "Priya", "Anjali", "Karan", "Rahul"]
    last_names = ["Sharma", "Verma", "Kumar", "Singh", "Patel", "Reddy", "Rao", "Joshi", "Iyer", "Banerjee"]
    party_a = f"{random.choice(first_names)} {random.choice(last_names)}"
    party_b = f"{random.choice(first_names)} {random.choice(last_names)}"
    case_name = f"{party_a} v. {party_b}"
    
    # Suffix year to case name
    case_year = random.randint(2018, 2024)
    case_name_full = f"{case_name} ({case_year})"
    
    # State and court
    state = random.choice(scen["states"])
    court = random.choice(scen["court"])
    
    # Custom details
    cases_data.append({
        "case_id": case_id,
        "case_name": case_name_full,
        "court": court,
        "state": state,
        "case_type": cat,
        "judgment_date": f"{case_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        "acts": scen["acts"],
        "sections": scen["sections"],
        "keywords": scen["keywords"],
        "facts": fact_text,
        "legal_issue": f"Whether the respondent is liable under provisions of {scen['acts']} for the claimed dispute.",
        "arguments": outcome_meta["arguments"],
        "evidence": outcome_meta["evidence"],
        "judgment_summary": outcome_meta["judgment"],
        "outcome": outcome_meta["outcome"],
        "precedent": f"Precedent Case Citation {random.randint(10,99)} SCC {random.randint(100,999)}",
        "source_url": f"https://www.indiankanoon.org/doc/{random.randint(1000000, 9999999)}",
        "verified": "True" if random.random() > 0.1 else "False" # 90% verified, 10% unverified
    })
    case_id += 1

df_cases = pd.DataFrame(cases_data)
df_cases.to_csv("H:/intern/project/nyaya-ai/data/demo/legal_cases.csv", index=False)
print("Generated", len(df_cases), "cases.")
