import urllib.request
import json
import re
import os

def get_part_and_chapter(art_num_str):
    if art_num_str == "0" or art_num_str.lower() == "preamble":
        return "Preamble", None
        
    match = re.match(r'^(\d+)', art_num_str)
    if not match:
        return "Unknown", None
    base = int(match.group(1))
    
    if art_num_str == "51A":
        return "Part IVA - Fundamental Duties", None
    
    if 1 <= base <= 4:
        return "Part I - The Union and its Territory", None
    elif 5 <= base <= 11:
        return "Part II - Citizenship", None
    elif 12 <= base <= 35:
        return "Part III - Fundamental Rights", None
    elif base == 51:
        return "Part IV - Directive Principles of State Policy", None
    elif 36 <= base <= 50:
        return "Part IV - Directive Principles of State Policy", None
    elif 52 <= base <= 151:
        part = "Part V - The Union"
        if 52 <= base <= 78:
            return part, "Chapter I - The Executive"
        elif 79 <= base <= 122:
            return part, "Chapter II - Parliament"
        elif base == 123:
            return part, "Chapter III - Legislative Powers of the President"
        elif 124 <= base <= 147:
            return part, "Chapter IV - The Union Judiciary"
        else:
            return part, "Chapter V - Comptroller and Auditor-General of India"
    elif 152 <= base <= 237:
        part = "Part VI - The States"
        if base == 152:
            return part, "Chapter I - General"
        elif 153 <= base <= 167:
            return part, "Chapter II - The Executive"
        elif 168 <= base <= 212:
            return part, "Chapter III - The State Legislature"
        elif base == 213:
            return part, "Chapter IV - Legislative Power of the Governor"
        elif 214 <= base <= 232:
            return part, "Chapter V - The High Courts in the States"
        else:
            return part, "Chapter VI - Subordinate Courts"
    elif base == 238:
        return "Part VII - The States in Part B of the First Schedule", None
    elif 239 <= base <= 242:
        return "Part VIII - The Union Territories", None
    elif art_num_str.startswith("243") and len(art_num_str) > 3:
        sub = art_num_str[3:]
        sub_upper = sub.upper()
        if sub_upper <= "O":
            return "Part IX - The Panchayats", None
        elif "P" <= sub_upper <= "ZG" or (len(sub_upper) == 2 and sub_upper[0] == "Z" and sub_upper[1] <= "G"):
            return "Part IXA - The Municipalities", None
        else:
            return "Part IXB - Co-operative Societies", None
    elif base == 243:
        return "Part IX - The Panchayats", None
    elif 244 <= base <= 244:
        return "Part X - The Scheduled and Tribal Areas", None
    elif 245 <= base <= 263:
        part = "Part XI - Relations between the Union and the States"
        if 245 <= base <= 255:
            return part, "Chapter I - Legislative Relations"
        else:
            return part, "Chapter II - Administrative Relations"
    elif base == 300 or art_num_str == "300A":
        part = "Part XII - Finance, Property, Contracts and Suits"
        if art_num_str == "300A":
            return part, "Chapter IV - Right to Property"
        else:
            return part, "Chapter III - Property, Contracts, Rights, Liabilities, Obligations and Suits"
    elif 264 <= base <= 300:
        part = "Part XII - Finance, Property, Contracts and Suits"
        if 264 <= base <= 291:
            return part, "Chapter I - Finance"
        elif 292 <= base <= 293:
            return part, "Chapter II - Borrowing"
        else:
            return part, "Chapter III - Property, Contracts, Rights, Liabilities, Obligations and Suits"
    elif 301 <= base <= 307:
        return "Part XIII - Trade, Commerce and Intercourse within the Territory of India", None
    elif 308 <= base <= 323:
        part = "Part XIV - Services under the Union and the States"
        if 308 <= base <= 314:
            return part, "Chapter I - Services"
        else:
            return part, "Chapter II - Public Service Commissions"
    elif base == 323:
        return "Part XIVA - Tribunals", None
    elif 324 <= base <= 329:
        return "Part XV - Elections", None
    elif 330 <= base <= 342:
        return "Part XVI - Special Provisions relating to Certain Classes", None
    elif 343 <= base <= 351:
        part = "Part XVII - Official Language"
        if 343 <= base <= 344:
            return part, "Chapter I - Language of the Union"
        elif 345 <= base <= 347:
            return part, "Chapter II - Regional Languages"
        elif 348 <= base <= 349:
            return part, "Chapter III - Language of the Supreme Court, High Courts, etc."
        else:
            return part, "Chapter IV - Special Directives"
    elif 352 <= base <= 360:
        return "Part XVIII - Emergency Provisions", None
    elif 361 <= base <= 367:
        return "Part XIX - Miscellaneous", None
    elif base == 368:
        return "Part XX - Amendment of the Constitution", None
    elif 369 <= base <= 392:
        return "Part XXI - Temporary, Transitional and Special Provisions", None
    elif 393 <= base <= 395:
        return "Part XXII - Short Title, Commencement, Authoritative Text in Hindi and Repeals", None
    else:
        return "Unknown", None

def main():
    print("Fetching raw constitutional articles from civictech-India...")
    url = "https://raw.githubusercontent.com/civictech-India/constitution-of-india/main/constitution_of_india.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        raw_data = json.load(response)
    print(f"Downloaded {len(raw_data)} raw records.")

    # Original annotated articles 14, 19, 21, 22, 25, 32
    original_articles = {
        "14": {
            "article_number": "14",
            "title": "Equality before law",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.",
            "fundamental_right": "Right to Equality",
            "constitutional_part": "Part III",
            "related_articles": ["15", "16", "17", "18"],
            "clauses": [
                {
                    "clause_id": "art_14_child_0",
                    "clause": "14",
                    "text": "Equality before law: The State shall not deny to any person equality before the law within the territory of India. This means that all individuals, whether citizens or foreigners, are subject to the same ordinary law of the land, and no one is above the law. It prohibits arbitrary discrimination by the State.",
                    "category": "Equality",
                    "keywords": ["equality before law", "rule of law", "non-arbitrariness", "discrimination"],
                    "legal_topics": ["Equality before Law", "Rule of Law", "Arbitrariness"],
                    "related_cases": ["Kesavananda Bharati v. State of Kerala", "Maneka Gandhi v. Union of India"]
                },
                {
                    "clause_id": "art_14_child_1",
                    "clause": "14",
                    "text": "Equal protection of the laws: The State shall not deny to any person the equal protection of the laws within the territory of India. This requires that likes should be treated alike, meaning people under similar circumstances should receive similar legal treatment. Reasonable classification is permitted, but class legislation is prohibited.",
                    "category": "Equality",
                    "keywords": ["equal protection", "reasonable classification", "discrimination", "likes alike"],
                    "legal_topics": ["Equal Protection of the Laws", "Reasonable Classification", "Anti-discrimination"],
                    "related_cases": ["State of West Bengal v. Anwar Ali Sarkar"]
                }
            ]
        },
        "19": {
            "article_number": "19",
            "title": "Protection of certain rights regarding freedom of speech, etc.",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "All citizens shall have the right— (a) to freedom of speech and expression; (b) to assemble peaceably and without arms; (c) to form associations or unions; (d) to move freely throughout the territory of India; (e) to reside and settle in any part of the territory of India; and (g) to practise any profession, or to carry on any occupation, trade or business.",
            "fundamental_right": "Right to Freedom",
            "constitutional_part": "Part III",
            "related_articles": ["20", "21", "22"],
            "clauses": [
                {
                    "clause_id": "art_19_child_0",
                    "clause": "19(1)(a)",
                    "text": "Freedom of speech and expression: All citizens shall have the right to freedom of speech and expression. This includes the right to express one's views, opinions, beliefs, and convictions freely by word of mouth, writing, printing, picturing, or in any other manner. It also covers freedom of the press, the right to remain silent, and the right to access information.",
                    "category": "Speech",
                    "keywords": ["freedom of speech", "expression", "press freedom", "opinion", "access information"],
                    "legal_topics": ["Freedom of Speech and Expression", "Freedom of the Press", "Right to Information"],
                    "related_cases": ["Shreya Singhal v. Union of India", "Maneka Gandhi v. Union of India"]
                },
                {
                    "clause_id": "art_19_child_1",
                    "clause": "19(1)(b)",
                    "text": "Freedom of peaceful assembly: All citizens shall have the right to assemble peaceably and without arms. This includes the right to hold public meetings, demonstrations, and take out processions. It does not include the right to strike, and the assembly must be peaceful and unarmed, subject to reasonable public order restrictions.",
                    "category": "Assembly",
                    "keywords": ["peaceful assembly", "protest", "procession", "public order", "demonstration"],
                    "legal_topics": ["Freedom of Peaceful Assembly", "Right to Protest", "Public Order Restrictions"],
                    "related_cases": ["Babulal Parate v. State of Maharashtra"]
                },
                {
                    "clause_id": "art_19_child_2",
                    "clause": "19(1)(c)",
                    "text": "Freedom of association: All citizens shall have the right to form associations, unions, or co-operative societies. This includes the right to form political parties, companies, partnership firms, clubs, organizations, or trade unions. The right also covers the negative right of not joining an association.",
                    "category": "Association",
                    "keywords": ["freedom of association", "unions", "cooperative societies", "political parties", "trade unions"],
                    "legal_topics": ["Freedom of Association", "Trade Union Rights"],
                    "related_cases": ["All India Bank Employees' Association v. National Industrial Tribunal"]
                },
                {
                    "clause_id": "art_19_child_3",
                    "clause": "19(2)",
                    "text": "Reasonable restrictions on speech: The State can impose reasonable restrictions on freedom of speech and expression under Article 19(2). These restrictions can only be imposed on specific grounds: the sovereignty and integrity of India, the security of the State, friendly relations with foreign States, public order, decency or morality, contempt of court, defamation, or incitement to an offence.",
                    "category": "Speech Restrictions",
                    "keywords": ["reasonable restrictions", "sovereignty", "public order", "morality", "defamation", "contempt of court", "security of state"],
                    "legal_topics": ["Reasonable Restrictions", "Public Order Exceptions", "Defamation and Free Speech"],
                    "related_cases": ["Shreya Singhal v. Union of India"]
                }
            ]
        },
        "21": {
            "article_number": "21",
            "title": "Protection of life and personal liberty",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "No person shall be deprived of his life or personal liberty except according to procedure established by law.",
            "fundamental_right": "Right to Life and Personal Liberty",
            "constitutional_part": "Part III",
            "related_articles": ["19", "20", "22"],
            "clauses": [
                {
                    "clause_id": "art_21_child_0",
                    "clause": "21",
                    "text": "Protection of life and personal liberty: No person shall be deprived of his life or personal liberty except according to procedure established by law. This article is the cornerstone of fundamental rights, ensuring that a person's life and liberty cannot be encroached upon by arbitrary executive actions. The term 'life' is interpreted broadly to mean a life with human dignity, not just animal existence.",
                    "category": "Liberty",
                    "keywords": ["right to life", "personal liberty", "human dignity", "procedure established by law", "due process"],
                    "legal_topics": ["Personal Liberty", "Human Dignity", "Procedure Established by Law"],
                    "related_cases": ["Maneka Gandhi v. Union of India", "Kesavananda Bharati v. State of Kerala"]
                },
                {
                    "clause_id": "art_21_child_1",
                    "clause": "21",
                    "text": "Right to privacy under Article 21: The right to privacy is protected as an intrinsic part of the right to life and personal liberty. It protects individual autonomy, informational privacy, spatial privacy (like freedom from unwarranted search and wiretapping), and bodily integrity. Any state intrusion into privacy must be backed by law, have a legitimate aim, and be proportional.",
                    "category": "Privacy",
                    "keywords": ["right to privacy", "privacy", "surveillance", "wiretapping", "search warrant", "informational privacy"],
                    "legal_topics": ["Right to Privacy", "Informational Privacy", "Autonomy"],
                    "related_cases": ["Justice K.S. Puttaswamy v. Union of India"]
                }
            ]
        },
        "22": {
            "article_number": "22",
            "title": "Protection against arrest and detention in certain cases",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest nor shall he be denied the right to consult, and to be defended by, a legal practitioner of his choice.",
            "fundamental_right": "Right to Freedom",
            "constitutional_part": "Part III",
            "related_articles": ["21"],
            "clauses": [
                {
                    "clause_id": "art_22_child_0",
                    "clause": "22(1)",
                    "text": "Rights of arrested persons to grounds of arrest and legal counsel: Every arrested person has the right to be informed as soon as possible of the grounds for their arrest and cannot be denied the right to consult and be defended by a legal practitioner of their choice.",
                    "category": "Arrest",
                    "keywords": ["arrest", "grounds of arrest", "legal counsel", "defense lawyer", "police custody"],
                    "legal_topics": ["Arrest Safeguards", "Right to Legal Counsel"],
                    "related_cases": ["D.K. Basu v. State of West Bengal", "Joginder Kumar v. State of UP"]
                },
                {
                    "clause_id": "art_22_child_1",
                    "clause": "22(2)",
                    "text": "Production before magistrate within 24 hours: Every person who is arrested and detained in custody must be produced before the nearest magistrate within a period of twenty-four hours of such arrest, excluding the time necessary for the journey, and no such person shall be detained in custody beyond the said period without the authority of a magistrate.",
                    "category": "Arrest",
                    "keywords": ["production before magistrate", "24 hours", "magistrate warrant", "detention limit", "habeas corpus"],
                    "legal_topics": ["Magistrate Production", "Detention Limit"],
                    "related_cases": ["D.K. Basu v. State of West Bengal", "State of Punjab v. Ajaib Singh"]
                }
            ]
        },
        "25": {
            "article_number": "25",
            "title": "Freedom of conscience and free profession, practice and propagation of religion",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "Subject to public order, morality and health and to the other provisions of this Part, all persons are equally entitled to freedom of conscience and the right freely to profess, practise and propagate religion.",
            "fundamental_right": "Right to Freedom of Religion",
            "constitutional_part": "Part III",
            "related_articles": ["26", "27", "28"],
            "clauses": [
                {
                    "clause_id": "art_25_child_0",
                    "clause": "25(1)",
                    "text": "Freedom of religion: Subject to public order, morality, and health, all persons are equally entitled to freedom of conscience and the right freely to profess, practise, and propagate religion. This guarantees the right to perform religious rituals, wear religious symbols, and spread religious tenets, but prohibits forced conversions.",
                    "category": "Religion",
                    "keywords": ["freedom of religion", "profess", "practice", "propagate", "freedom of conscience", "essential practices"],
                    "legal_topics": ["Freedom of Religion", "Freedom of Conscience", "Religious Expression"],
                    "related_cases": ["Bijoe Emmanuel v. State of Kerala", "Sabarimala Case"]
                }
            ]
        },
        "32": {
            "article_number": "32",
            "title": "Remedies for enforcement of rights conferred by this Part",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed. The Supreme Court shall have power to issue directions or orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, whichever may be appropriate.",
            "fundamental_right": "Right to Constitutional Remedies",
            "constitutional_part": "Part III",
            "related_articles": ["226"],
            "clauses": [
                {
                    "clause_id": "art_32_child_0",
                    "clause": "32",
                    "text": "Writ remedies in the Supreme Court: The right to move the Supreme Court by appropriate proceedings for the enforcement of Fundamental Rights is guaranteed. The Court has the power to issue writs, including habeas corpus (to challenge illegal detention), mandamus (to direct public duty), prohibition, quo warranto, and certiorari (to quash judicial orders). This is described by Dr. B.R. Ambedkar as the heart and soul of the Constitution.",
                    "category": "Remedies",
                    "keywords": ["writ", "habeas corpus", "mandamus", "certiorari", "quo warranto", "supreme court", "fundamental rights enforcement"],
                    "legal_topics": ["Writ Jurisdiction", "Constitutional Remedies", "Fundamental Rights Enforcement"],
                    "related_cases": ["L. Chandra Kumar v. Union of India", "Kesavananda Bharati v. State of Kerala"]
                }
            ]
        }
    }

    # Newly annotated key articles
    new_annotated_articles = {
        "15": {
            "article_number": "15",
            "title": "Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "The State shall not discriminate against any citizen on grounds only of religion, race, caste, sex, place of birth or any of them. Nothing in this article shall prevent the State from making any special provision for women and children, or for the advancement of any socially and educationally backward classes of citizens or for the Scheduled Castes and the Scheduled Tribes.",
            "fundamental_right": "Right to Equality",
            "constitutional_part": "Part III",
            "related_articles": ["14", "16", "29"],
            "clauses": [
                {
                    "clause_id": "art_15_child_0",
                    "clause": "15(1)",
                    "text": "Prohibition of discrimination: The State shall not discriminate against any citizen on grounds only of religion, race, caste, sex, place of birth or any of them. It ensures equal access to public places like shops, restaurants, wells, and roads.",
                    "category": "Equality",
                    "keywords": ["discrimination", "equal access", "caste discrimination", "gender discrimination"],
                    "legal_topics": ["Prohibition of Discrimination", "Equal Access Rights"],
                    "related_cases": ["State of Madras v. Champakam Dorairajan"]
                },
                {
                    "clause_id": "art_15_child_1",
                    "clause": "15(4)",
                    "text": "Reservation and special provisions: Nothing in this article shall prevent the State from making any special provision for the advancement of any socially and educationally backward classes of citizens or for the Scheduled Castes and the Scheduled Tribes. This forms the basis of educational reservations.",
                    "category": "Equality",
                    "keywords": ["reservation", "affirmative action", "backward classes", "scheduled castes", "scheduled tribes"],
                    "legal_topics": ["Reservation in Education", "Affirmative Action"],
                    "related_cases": ["Indra Sawhney v. Union of India"]
                }
            ]
        },
        "16": {
            "article_number": "16",
            "title": "Equality of opportunity in matters of public employment",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State. Nothing in this article shall prevent the State from making any provision for the reservation of appointments or posts in favour of any backward class of citizens.",
            "fundamental_right": "Right to Equality",
            "constitutional_part": "Part III",
            "related_articles": ["14", "15"],
            "clauses": [
                {
                    "clause_id": "art_16_child_0",
                    "clause": "16(1)",
                    "text": "Equality of opportunity in jobs: There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State.",
                    "category": "Equality",
                    "keywords": ["equality of opportunity", "public employment", "state job equality"],
                    "legal_topics": ["Equality in Public Employment"],
                    "related_cases": ["Indra Sawhney v. Union of India"]
                },
                {
                    "clause_id": "art_16_child_1",
                    "clause": "16(4)",
                    "text": "Job reservation for backward classes: Nothing in this article shall prevent the State from making any provision for the reservation of appointments or posts in favour of any backward class of citizens which, in the opinion of the State, is not adequately represented in the services under the State.",
                    "category": "Equality",
                    "keywords": ["reservation in jobs", "public employment reservation", "backward class representation"],
                    "legal_topics": ["Reservation in Public Employment", "Adequacy of Representation"],
                    "related_cases": ["Indra Sawhney v. Union of India", "M. Nagaraj v. Union of India", "Jarnail Singh v. Lachhmi Narain Gupta"]
                }
            ]
        },
        "21A": {
            "article_number": "21A",
            "title": "Right to education",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "The State shall provide free and compulsory education to all children of the age of six to fourteen years in such manner as the State may, by law, determine.",
            "fundamental_right": "Right to Life and Personal Liberty",
            "constitutional_part": "Part III",
            "related_articles": ["21", "45"],
            "clauses": [
                {
                    "clause_id": "art_21a_child_0",
                    "clause": "21A",
                    "text": "Free and compulsory education: The State shall provide free and compulsory education to all children of the age of six to fourteen years in such manner as the State may, by law, determine. It guarantees primary education as a fundamental right.",
                    "category": "Education",
                    "keywords": ["right to education", "free education", "compulsory education", "school child rights", "six to fourteen years"],
                    "legal_topics": ["Right to Education", "Child Rights"],
                    "related_cases": ["Mohini Jain v. State of Karnataka", "Unni Krishnan v. State of AP", "Pramati Educational and Cultural Trust v. Union of India"]
                }
            ]
        },
        "26": {
            "article_number": "26",
            "title": "Freedom to manage religious affairs",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "Subject to public order, morality and health, every religious denomination or any section thereof shall have the right— (a) to establish and maintain institutions for religious and charitable purposes; (b) to manage its own affairs in matters of religion; (c) to own and acquire movable and immovable property; and (d) to administer such property in accordance with law.",
            "fundamental_right": "Right to Freedom of Religion",
            "constitutional_part": "Part III",
            "related_articles": ["25", "27", "28"],
            "clauses": [
                {
                    "clause_id": "art_26_child_0",
                    "clause": "26",
                    "text": "Religious institutional rights: Every religious denomination has the right to establish and maintain religious/charitable institutions, manage its own religious affairs, own and acquire property, and administer such property in accordance with law, subject to public order, morality, and health.",
                    "category": "Religion",
                    "keywords": ["religious denomination", "manage affairs", "religious property", "charitable institution"],
                    "legal_topics": ["Freedom to Manage Religious Affairs", "Denominational Rights"],
                    "related_cases": ["Shirur Mutt Case", "Sabarimala Case"]
                }
            ]
        },
        "27": {
            "article_number": "27",
            "title": "Freedom as to payment of taxes for promotion of any particular religion",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "No person shall be compelled to pay any taxes, the proceeds of which are specifically appropriated in payment of expenses for the promotion or maintenance of any particular religion or religious denomination.",
            "fundamental_right": "Right to Freedom of Religion",
            "constitutional_part": "Part III",
            "related_articles": ["25", "26"],
            "clauses": [
                {
                    "clause_id": "art_27_child_0",
                    "clause": "27",
                    "text": "Secular taxation safeguards: No citizen can be compelled to pay taxes meant specifically for the promotion or maintenance of any particular religion, ensuring state neutrality in religious funding.",
                    "category": "Religion",
                    "keywords": ["tax for religion", "secularism", "compulsory tax", "religious promotion"],
                    "legal_topics": ["Secular Funding Neutrality", "Freedom from Religious Tax"],
                    "related_cases": ["Shirur Mutt Case"]
                }
            ]
        },
        "28": {
            "article_number": "28",
            "title": "Freedom as to attendance at religious instruction or religious worship in certain educational institutions",
            "part": "Part III - Fundamental Rights",
            "chapter": None,
            "full_text": "No religious instruction shall be provided in any educational institution wholly maintained out of State funds. No person attending any educational institution recognised by the State or receiving aid out of State funds shall be required to take part in any religious instruction.",
            "fundamental_right": "Right to Freedom of Religion",
            "constitutional_part": "Part III",
            "related_articles": ["25", "26", "27"],
            "clauses": [
                {
                    "clause_id": "art_28_child_0",
                    "clause": "28",
                    "text": "Religious instruction bans in state schools: Bans religious instruction in educational institutions wholly maintained out of State funds. Protects students in state-aided schools from forced attendance at religious instruction or worship.",
                    "category": "Religion",
                    "keywords": ["religious instruction", "state funds school", "state-aided school", "compulsory worship"],
                    "legal_topics": ["Religious Instruction in Schools", "Secular Education"],
                    "related_cases": ["Bijoe Emmanuel v. State of Kerala"]
                }
            ]
        },
        "131": {
            "article_number": "131",
            "title": "Original jurisdiction of the Supreme Court",
            "part": "Part V - The Union",
            "chapter": "Chapter IV - The Union Judiciary",
            "full_text": "Subject to the provisions of this Constitution, the Supreme Court shall, to the exclusion of any other court, have original jurisdiction in any dispute— (a) between the Government of India and one or more States; or (b) between the Government of India and any State or States on one side and one or more other States on the other; or (c) between two or more States.",
            "fundamental_right": "",
            "constitutional_part": "Part V",
            "related_articles": ["136", "262"],
            "clauses": [
                {
                    "clause_id": "art_131_child_0",
                    "clause": "131",
                    "text": "Federal original jurisdiction: The Supreme Court has exclusive original jurisdiction in disputes between the Center and States, or between different States, involving any question of law or fact on which the existence of a legal right depends.",
                    "category": "Federal disputes",
                    "keywords": ["original jurisdiction", "center-state dispute", "inter-state dispute", "federalism"],
                    "legal_topics": ["Original Jurisdiction", "Federal Disputes"],
                    "related_cases": ["State of West Bengal v. Union of India", "State of Karnataka v. Union of India"]
                }
            ]
        },
        "226": {
            "article_number": "226",
            "title": "Power of High Courts to issue certain writs",
            "part": "Part VI - The States",
            "chapter": "Chapter V - The High Courts in the States",
            "full_text": "Notwithstanding anything in article 32, every High Court shall have power, throughout the territories in relation to which it exercises jurisdiction, to issue to any person or authority, including in appropriate cases any Government, within those territories directions, orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, or any of them, for the enforcement of any of the rights conferred by Part III and for any other purpose.",
            "fundamental_right": "",
            "constitutional_part": "Part VI",
            "related_articles": ["32"],
            "clauses": [
                {
                    "clause_id": "art_226_child_0",
                    "clause": "226",
                    "text": "Writ jurisdiction of High Courts: Empowers High Courts to issue writs for the enforcement of fundamental rights under Part III, as well as 'for any other purpose' (which includes ordinary legal rights), giving them a broader writ scope than the Supreme Court.",
                    "category": "Constitutional remedies",
                    "keywords": ["writ", "high court", "habeas corpus", "mandamus", "certiorari", "judicial review", "any other purpose"],
                    "legal_topics": ["Writ Jurisdiction of High Courts", "Constitutional Remedies"],
                    "related_cases": ["L. Chandra Kumar v. Union of India", "State of UP v. Mohammad Nooh"]
                }
            ]
        },
        "262": {
            "article_number": "262",
            "title": "Adjudication of disputes relating to waters of inter-State rivers or river valleys",
            "part": "Part XI - Relations between the Union and the States",
            "chapter": "Chapter II - Administrative Relations",
            "full_text": "Parliament may by law provide for the adjudication of any dispute or complaint with respect to the use, distribution or control of the waters of, or in, any inter-State river or river valley. Notwithstanding anything in this Constitution, Parliament may by law provide that neither the Supreme Court nor any other court shall exercise jurisdiction in respect of any such dispute or complaint.",
            "fundamental_right": "",
            "constitutional_part": "Part XI",
            "related_articles": ["131"],
            "clauses": [
                {
                    "clause_id": "art_262_child_0",
                    "clause": "262",
                    "text": "Inter-state river water disputes: Enables Parliament to create laws to adjudicate inter-state river or river valley disputes, and exclude the jurisdiction of the Supreme Court and other courts over such disputes, leading to the creation of Inter-State Water Disputes Tribunals.",
                    "category": "Federal disputes",
                    "keywords": ["river water", "water sharing", "inter-state river", "water tribunal", "court jurisdiction exclusion"],
                    "legal_topics": ["Inter-State River Water Disputes", "Federal Water Sharing"],
                    "related_cases": ["State of Karnataka v. State of Andhra Pradesh"]
                }
            ]
        },
        "300A": {
            "article_number": "300A",
            "title": "Persons not to be deprived of property save by authority of law",
            "part": "Part XII - Finance, Property, Contracts and Suits",
            "chapter": "Chapter IV - Right to Property",
            "full_text": "No person shall be deprived of his property save by authority of law.",
            "fundamental_right": "",
            "constitutional_part": "Part XII",
            "related_articles": [],
            "clauses": [
                {
                    "clause_id": "art_300a_child_0",
                    "clause": "300A",
                    "text": "Right to property: While the right to property was deleted as a fundamental right by the 44th Amendment, Article 300A protects it as a constitutional/legal right, ensuring that the state cannot acquire a person's property without a clear valid law enacted by a legislature.",
                    "category": "Property",
                    "keywords": ["right to property", "property acquisition", "authority of law", "compensation", "eminent domain"],
                    "legal_topics": ["Right to Property", "Eminent Domain"],
                    "related_cases": ["Jilubhai Nanbhai Khachar v. State of Gujarat", "K.T. Plantation Pvt. Ltd. v. State of Karnataka"]
                }
            ]
        },
        "324": {
            "article_number": "324",
            "title": "Superintendence, direction and control of elections to be vested in an Election Commission",
            "part": "Part XV - Elections",
            "chapter": None,
            "full_text": "The superintendence, direction and control of the preparation of the electoral rolls for, and the conduct of, all elections to Parliament and to the Legislature of every State and of elections to the offices of President and Vice-President held under this Constitution shall be vested in a Commission.",
            "fundamental_right": "",
            "constitutional_part": "Part XV",
            "related_articles": ["325", "326", "329"],
            "clauses": [
                {
                    "clause_id": "art_324_child_0",
                    "clause": "324",
                    "text": "Powers of the Election Commission: Vests the superintendence, direction, and control of elections to Parliament, State Legislatures, and offices of President and Vice-President in the Election Commission of India, giving it independent plenary powers to ensure free and fair elections.",
                    "category": "Elections",
                    "keywords": ["election commission", "free and fair elections", "preparation of rolls", "conduct of elections", "electoral rolls"],
                    "legal_topics": ["Election Commission Powers", "Conduct of Elections"],
                    "related_cases": ["Mohinder Singh Gill v. Chief Election Commissioner", "T.N. Seshan v. Union of India"]
                }
            ]
        },
        "352": {
            "article_number": "352",
            "title": "Proclamation of Emergency",
            "part": "Part XVIII - Emergency Provisions",
            "chapter": None,
            "full_text": "If the President is satisfied that a grave emergency exists whereby the security of India or of any part of the territory thereof is threatened, whether by war or external aggression or armed rebellion, he may, by Proclamation, make a declaration to that effect.",
            "fundamental_right": "",
            "constitutional_part": "Part XVIII",
            "related_articles": ["353", "358", "359"],
            "clauses": [
                {
                    "clause_id": "art_352_child_0",
                    "clause": "352",
                    "text": "National Emergency proclamation: President can proclaim a National Emergency if the security of India or any part of it is threatened by war, external aggression, or armed rebellion, leading to centralizing of federal powers and potential suspension of fundamental rights under Article 359.",
                    "category": "Emergency",
                    "keywords": ["national emergency", "war", "external aggression", "armed rebellion", "proclamation", "rights suspension"],
                    "legal_topics": ["National Emergency", "Emergency Powers"],
                    "related_cases": ["A.D.M. Jabalpur v. Shivkant Shukla", "Minerva Mills v. Union of India"]
                }
            ]
        },
        "356": {
            "article_number": "356",
            "title": "Provisions in case of failure of constitutional machinery in States",
            "part": "Part XVIII - Emergency Provisions",
            "chapter": None,
            "full_text": "If the President, on receipt of a report from the Governor of a State or otherwise, is satisfied that a situation has arisen in which the government of the State cannot be carried on in accordance with the provisions of this Constitution, the President may by Proclamation assume to himself all or any of the functions of the Government of the State.",
            "fundamental_right": "",
            "constitutional_part": "Part XVIII",
            "related_articles": ["357", "365"],
            "clauses": [
                {
                    "clause_id": "art_356_child_0",
                    "clause": "356",
                    "text": "President's Rule in States: Empowers the President to dismiss a State Government and assume state executive functions (President's Rule) if the state government cannot function in accordance with the Constitution. Subject to strict judicial review.",
                    "category": "Emergency",
                    "keywords": ["president rule", "constitutional machinery failure", "governor report", "state assembly dissolution"],
                    "legal_topics": ["President's Rule", "Federalism Breakdown"],
                    "related_cases": ["S.R. Bommai v. Union of India", "State of Rajasthan v. Union of India"]
                }
            ]
        },
        "360": {
            "article_number": "360",
            "title": "Provisions as to financial emergency",
            "part": "Part XVIII - Emergency Provisions",
            "chapter": None,
            "full_text": "If the President is satisfied that a situation has arisen whereby the financial stability or credit of India or of any part of the territory thereof is threatened, he may, by a Proclamation, make a declaration to that effect.",
            "fundamental_right": "",
            "constitutional_part": "Part XVIII",
            "related_articles": [],
            "clauses": [
                {
                    "clause_id": "art_360_child_0",
                    "clause": "360",
                    "text": "Financial Emergency proclamation: Allows the President to declare a Financial Emergency if financial stability or credit of India is threatened, enabling reduction of salaries of public officials (including judges) and redirection of money bills.",
                    "category": "Emergency",
                    "keywords": ["financial emergency", "credit threat", "salary cut", "financial stability"],
                    "legal_topics": ["Financial Emergency"],
                    "related_cases": []
                }
            ]
        },
        "368": {
            "article_number": "368",
            "title": "Power of Parliament to amend the Constitution and procedure therefor",
            "part": "Part XX - Amendment of the Constitution",
            "chapter": None,
            "full_text": "Notwithstanding anything in this Constitution, Parliament may in exercise of its constituent power amend by way of addition, variation or repeal any provision of this Constitution in accordance with the procedure laid down in this article.",
            "fundamental_right": "",
            "constitutional_part": "Part XX",
            "related_articles": [],
            "clauses": [
                {
                    "clause_id": "art_368_child_0",
                    "clause": "368",
                    "text": "Parliamentary power to amend: Outlines Parliament's power to amend the Constitution by addition, variation, or repeal. Certain amendments require a special majority, and others require ratification by at least half of the state legislatures. Amendments cannot destroy the Basic Structure.",
                    "category": "Constitutional remedies",
                    "keywords": ["constitutional amendment", "constituent power", "special majority", "basic structure", "amendment procedure"],
                    "legal_topics": ["Power of Amendment", "Basic Structure Doctrine", "Procedure for Amendment"],
                    "related_cases": ["Kesavananda Bharati v. State of Kerala", "Minerva Mills v. Union of India", "Sajjan Singh v. State of Rajasthan"]
                }
            ]
        }
    }

    # Schedules definitions
    schedules = [
        {
            "article_number": "Schedule 1",
            "title": "First Schedule: States and Union Territories",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Lists the states and union territories of India, their names, territories, and jurisdictional areas.",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["1", "4"],
            "clauses": [{
                "clause_id": "sch_1_child_0",
                "clause": "Schedule 1",
                "text": "First Schedule: Lists 28 states and 8 union territories of India, detailing their territorial extents, names, and limits.",
                "category": "Federal Structure",
                "keywords": ["states list", "union territories", "territorial extent", "borders"],
                "legal_topics": ["Territory of India", "States and Union Territories"],
                "related_cases": []
            }]
        },
        {
            "article_number": "Schedule 2",
            "title": "Second Schedule: Emoluments, Salaries and Allowances",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Provisions as to the President, Governors, Speaker, Judges, Comptroller and Auditor-General.",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["59", "65", "75", "97", "125", "148", "158", "164", "186", "221"],
            "clauses": [{
                "clause_id": "sch_2_child_0",
                "clause": "Schedule 2",
                "text": "Second Schedule: Details salaries, emoluments, and allowances for high constitutional office holders of the Union and States.",
                "category": "Public Administration",
                "keywords": ["salaries", "emoluments", "allowances", "judges pay", "president salary"],
                "legal_topics": ["Salaries of Constitutional Officials"],
                "related_cases": []
            }]
        },
        {
            "article_number": "Schedule 3",
            "title": "Third Schedule: Forms of Oaths or Affirmations",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Forms of Oaths or Affirmations for Ministers, candidates for elections, members of parliament, judges.",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["75", "84", "99", "124", "146", "173", "188", "219"],
            "clauses": [{
                "clause_id": "sch_3_child_0",
                "clause": "Schedule 3",
                "text": "Third Schedule: Contains oath and affirmation texts for Union and State Ministers, MP and MLA candidates, judges, and CAG.",
                "category": "Constitutional Rituals",
                "keywords": ["oath", "affirmation", "sovereignty", "allegiance"],
                "legal_topics": ["Constitutional Oaths"],
                "related_cases": []
            }]
        },
        {
            "article_number": "Schedule 4",
            "title": "Fourth Schedule: Allocation of seats in Council of States",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Allocation of Rajya Sabha seats to each State and Union Territory.",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["4", "80"],
            "clauses": [{
                "clause_id": "sch_4_child_0",
                "clause": "Schedule 4",
                "text": "Fourth Schedule: Outlines the number of seats allocated to each State and Union Territory in the Rajya Sabha (Council of States).",
                "category": "Federal Representation",
                "keywords": ["rajya sabha", "seats allocation", "upper house", "state representation"],
                "legal_topics": ["Allocation of Seats in Rajya Sabha"],
                "related_cases": []
            }]
        },
        {
            "article_number": "Schedule 5",
            "title": "Fifth Schedule: Administration of Scheduled Areas and Tribes",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Provisions as to the Administration and Control of Scheduled Areas and Scheduled Tribes (except Northeast).",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["244"],
            "clauses": [{
                "clause_id": "sch_5_child_0",
                "clause": "Schedule 5",
                "text": "Fifth Schedule: Governs the administration of tribal areas in states other than Assam, Meghalaya, Tripura, and Mizoram. Establishes Tribes Advisory Councils.",
                "category": "Tribal Rights",
                "keywords": ["scheduled area", "tribes advisory council", "governor power", "tribal land protect"],
                "legal_topics": ["Administration of Scheduled Areas"],
                "related_cases": ["Samatha v. State of Andhra Pradesh"]
            }]
        },
        {
            "article_number": "Schedule 6",
            "title": "Sixth Schedule: Tribal Areas in Northeastern States",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Provisions as to the Administration of Tribal Areas in the States of Assam, Meghalaya, Tripura and Mizoram.",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["244", "275"],
            "clauses": [{
                "clause_id": "sch_6_child_0",
                "clause": "Schedule 6",
                "text": "Sixth Schedule: Allows creation of Autonomous District Councils (ADCs) in Assam, Meghalaya, Tripura, and Mizoram to protect tribal autonomy.",
                "category": "Tribal Autonomy",
                "keywords": ["autonomous district council", "northeast tribal", "local governance", "tribal culture"],
                "legal_topics": ["Autonomous District Councils", "Sixth Schedule Autonomy"],
                "related_cases": []
            }]
        },
        {
            "article_number": "Schedule 7",
            "title": "Seventh Schedule: Legislative Subject Lists",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Division of powers between Union and States: List I (Union), List II (State), List III (Concurrent).",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["246"],
            "clauses": [{
                "clause_id": "sch_7_child_0",
                "clause": "Schedule 7",
                "text": "Seventh Schedule: Distributes legislative powers into List I (Union List - defense, foreign affairs), List II (State List - police, public order), and List III (Concurrent List - education, forests).",
                "category": "Federal Division of Powers",
                "keywords": ["union list", "state list", "concurrent list", "legislative powers", "police state", "defence union"],
                "legal_topics": ["Division of Legislative Powers", "Federal Subject Lists"],
                "related_cases": ["Prafulla Kumar Mukherjee v. Bank of Commerce"]
            }]
        },
        {
            "article_number": "Schedule 8",
            "title": "Eighth Schedule: Recognized Languages",
            "part": "Schedules",
            "chapter": None,
            "full_text": "List of 22 official languages recognized by the Constitution of India.",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["344", "351"],
            "clauses": [{
                "clause_id": "sch_8_child_0",
                "clause": "Schedule 8",
                "text": "Eighth Schedule: Lists the 22 languages recognized by the Constitution for official purposes and promotion.",
                "category": "Linguistic Diversity",
                "keywords": ["official languages", "hindi", "tamil", "bengali", "sanskrit", "languages list"],
                "legal_topics": ["Recognized Languages"],
                "related_cases": []
            }]
        },
        {
            "article_number": "Schedule 9",
            "title": "Ninth Schedule: Validation of Acts and Regulations",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Contains laws protected from judicial review under Article 31B, subject to basic structure review.",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["31B"],
            "clauses": [{
                "clause_id": "sch_9_child_0",
                "clause": "Schedule 9",
                "text": "Ninth Schedule: Immunizes specific land reform and other acts from judicial review. Under I.R. Coelho, laws added post-1973 are subject to judicial review if they violate basic structure.",
                "category": "Judicial Immunity",
                "keywords": ["judicial review immunity", "land reforms", "article 31b", "basic structure review"],
                "legal_topics": ["Judicial Review Protection", "Land Reforms Preservation"],
                "related_cases": ["I.R. Coelho v. State of Tamil Nadu", "Waman Rao v. Union of India"]
            }]
        },
        {
            "article_number": "Schedule 10",
            "title": "Tenth Schedule: Anti-Defection Provisions",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Provisions as to disqualification on ground of defection (Anti-Defection Law, 52nd Amendment).",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["102", "191"],
            "clauses": [{
                "clause_id": "sch_10_child_0",
                "clause": "Schedule 10",
                "text": "Tenth Schedule: Disqualifies MPs and MLAs who defect from their political parties, vote against party whips, or voluntarily resign from their party.",
                "category": "Electoral Integrity",
                "keywords": ["defection", "anti-defection law", "party whip", "disqualification", "speaker decision"],
                "legal_topics": ["Anti-Defection Law", "Electoral Disqualification"],
                "related_cases": ["Kihoto Hollohan v. Zachillhu"]
            }]
        },
        {
            "article_number": "Schedule 11",
            "title": "Eleventh Schedule: Powers of Panchayats",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Specifies 29 subjects under the purview of Panchayats (73rd Amendment).",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["243G"],
            "clauses": [{
                "clause_id": "sch_11_child_0",
                "clause": "Schedule 11",
                "text": "Eleventh Schedule: Identifies 29 functional items (e.g. agriculture, education, sanitation) to be delegated to Panchayats.",
                "category": "Local Governance",
                "keywords": ["panchayat", "local self-government", "rural administration", "devolution"],
                "legal_topics": ["Panchayat Authority and Functions"],
                "related_cases": []
            }]
        },
        {
            "article_number": "Schedule 12",
            "title": "Twelfth Schedule: Powers of Municipalities",
            "part": "Schedules",
            "chapter": None,
            "full_text": "Specifies 18 subjects under the purview of Municipalities (74th Amendment).",
            "fundamental_right": "",
            "constitutional_part": "Schedules",
            "related_articles": ["243W"],
            "clauses": [{
                "clause_id": "sch_12_child_0",
                "clause": "Schedule 12",
                "text": "Twelfth Schedule: Identifies 18 functional items (e.g. urban planning, roads, waste management) delegated to Municipalities.",
                "category": "Local Governance",
                "keywords": ["municipality", "urban local bodies", "ward committees", "urban planning"],
                "legal_topics": ["Municipal Authority and Functions"],
                "related_cases": []
            }]
        }
    ]

    # Major amendments definitions
    amendments = [
        {
            "article_number": "Amendment 1",
            "title": "First Constitutional Amendment Act, 1951",
            "part": "Amendments",
            "chapter": None,
            "full_text": "Introduced the Ninth Schedule, created Articles 31A and 31B, and added reasonable restrictions (public order, friendly relations, incitement) to Article 19(2).",
            "fundamental_right": "",
            "constitutional_part": "Amendments",
            "related_articles": ["19", "31A", "31B"],
            "clauses": [{
                "clause_id": "am_1_child_0",
                "clause": "Amendment 1",
                "text": "First Amendment (1951): Inserted the Ninth Schedule and Article 31B to protect land reform laws from judicial review, and added 'public order', 'friendly relations with foreign states', and 'incitement to an offence' to Article 19(2) exceptions.",
                "category": "Amendments",
                "keywords": ["first amendment", "ninth schedule", "land reform protection", "speech restrictions"],
                "legal_topics": ["Constitutional Amendments", "Free Speech Restrictions"],
                "related_cases": ["Shankari Prasad v. Union of India", "Romesh Thappar v. State of Madras"]
            }]
        },
        {
            "article_number": "Amendment 42",
            "title": "Forty-Second Constitutional Amendment Act, 1976",
            "part": "Amendments",
            "chapter": None,
            "full_text": "Known as the Mini-Constitution. Added 'Socialist', 'Secular', and 'Integrity' to Preamble. Inserted Fundamental Duties (Part IVA). Attempted to elevate DPSPs over Fundamental Rights and limit judicial review.",
            "fundamental_right": "",
            "constitutional_part": "Amendments",
            "related_articles": ["51A", "368"],
            "clauses": [{
                "clause_id": "am_42_child_0",
                "clause": "Amendment 42",
                "text": "Forty-Second Amendment (1976): Added 'Secular', 'Socialist', and 'Integrity' to Preamble, inserted Part IVA (Fundamental Duties), and restricted judicial review powers of High Courts and Supreme Court (subsequently restored).",
                "category": "Amendments",
                "keywords": ["mini constitution", "secular", "socialist", "fundamental duties", "parliamentary supremacy"],
                "legal_topics": ["Major Amendments", "Preamble Revision", "Fundamental Duties"],
                "related_cases": ["Minerva Mills v. Union of India"]
            }]
        },
        {
            "article_number": "Amendment 44",
            "title": "Forty-Fourth Constitutional Amendment Act, 1978",
            "part": "Amendments",
            "chapter": None,
            "full_text": "Undid several undemocratic provisions of the 42nd Amendment. Removed Right to Property from Part III to Article 300A. Established that Articles 20 and 21 cannot be suspended during an Emergency.",
            "fundamental_right": "",
            "constitutional_part": "Amendments",
            "related_articles": ["20", "21", "300A", "352", "356"],
            "clauses": [{
                "clause_id": "am_44_child_0",
                "clause": "Amendment 44",
                "text": "Forty-Fourth Amendment (1978): Removed the Right to Property as a fundamental right (moving it to Article 300A), restricted the scope of National Emergency (replacing 'internal disturbance' with 'armed rebellion'), and prohibited suspension of Articles 20 and 21 during emergency.",
                "category": "Amendments",
                "keywords": ["forty-fourth amendment", "right to property removal", "emergency safeguards", "armed rebellion", "articles 20 21 protect"],
                "legal_topics": ["Emergency Safeguards", "Property Rights Migration"],
                "related_cases": []
            }]
        },
        {
            "article_number": "Amendment 86",
            "title": "Eighty-Sixth Constitutional Amendment Act, 2002",
            "part": "Amendments",
            "chapter": None,
            "full_text": "Made right to primary education a fundamental right under Article 21A, modified Article 45 DPSP, and added DPSP duty to parents under Article 51A(k).",
            "fundamental_right": "",
            "constitutional_part": "Amendments",
            "related_articles": ["21A", "45", "51A"],
            "clauses": [{
                "clause_id": "am_86_child_0",
                "clause": "Amendment 86",
                "text": "Eighty-Sixth Amendment (2002): Created Article 21A establishing the Right to Education for children aged 6 to 14, and added parent duties for education in Article 51A.",
                "category": "Amendments",
                "keywords": ["eighty-sixth amendment", "education right", "child education DPSP", "parent duty education"],
                "legal_topics": ["Education Rights Amendments"],
                "related_cases": ["Pramati Educational and Cultural Trust v. Union of India"]
            }]
        },
        {
            "article_number": "Amendment 103",
            "title": "One Hundred and Third Constitutional Amendment Act, 2019",
            "part": "Amendments",
            "chapter": None,
            "full_text": "Introduced 10% reservation for Economically Weaker Sections (EWS) in education and public employment by amending Articles 15 and 16.",
            "fundamental_right": "",
            "constitutional_part": "Amendments",
            "related_articles": ["15", "16"],
            "clauses": [{
                "clause_id": "am_103_child_0",
                "clause": "Amendment 103",
                "text": "103rd Amendment (2019): Enabled up to 10% reservations for Economically Weaker Sections (EWS) of citizens other than SC, ST, and OBCs.",
                "category": "Amendments",
                "keywords": ["ews reservation", "economically weaker sections", "103rd amendment", "reservation expansion"],
                "legal_topics": ["Affirmative Action Amendments", "EWS Quota"],
                "related_cases": ["Janhit Abhiyan v. Union of India"]
            }]
        }
    ]

    processed_articles = []
    
    # Track which article numbers we have seen to avoid duplicates
    seen_art_nos = set()
    
    # 1. Add original annotated articles
    for art_num, data in original_articles.items():
        processed_articles.append(data)
        seen_art_nos.add(art_num)
        
    # 2. Add new annotated articles
    for art_num, data in new_annotated_articles.items():
        processed_articles.append(data)
        seen_art_nos.add(art_num)

    # Helper function to extract keywords
    def extract_keywords_heuristic(text, title):
        words = re.findall(r'\b\w{4,}\b', text.lower() + " " + title.lower())
        stopwords = {
            "shall", "state", "under", "which", "after", "other", "every", "their", "there", 
            "where", "accord", "about", "those", "these", "person", "clause", "article",
            "provide", "court", "judge", "right", "constitution", "parliament", "government"
        }
        filtered = [w for w in words if w not in stopwords]
        # Get unique and take top 8
        unique = []
        for w in filtered:
            if w not in unique:
                unique.append(w)
        return unique[:8]

    # 3. Process raw articles
    for record in raw_data:
        art_val = str(record.get("article", ""))
        title = record.get("title", "").strip()
        description = record.get("description", "").strip()
        
        # If it's a number/alphanumeric article
        if not art_val or art_val == "0":
            continue # Preamble is handled or will be handled
            
        # Clean article number string (e.g. "Article 21" -> "21")
        art_num = art_val.replace("Article", "").strip()
        
        if art_num in seen_art_nos:
            continue # Skip, already have rich version
            
        part_name, chapter_name = get_part_and_chapter(art_num)
        
        # Determine if it's omitted
        is_omitted = "omitted" in description.lower() or "repealed" in title.lower() or "repealed" in description.lower()
        
        # Categories
        category = "General Provisions"
        if "jurisdiction" in title.lower() or "court" in title.lower() or "judge" in title.lower():
            category = "Judiciary"
        elif "service" in title.lower() or "commission" in title.lower():
            category = "Services"
        elif "tax" in title.lower() or "revenue" in title.lower() or "finance" in title.lower():
            category = "Finance"
        elif "trade" in title.lower() or "commerce" in title.lower():
            category = "Trade"
        elif "legislative" in title.lower() or "parliament" in title.lower():
            category = "Legislature"
        elif "president" in title.lower() or "governor" in title.lower():
            category = "Executive"
        elif is_omitted:
            category = "Omitted"
            
        kws = extract_keywords_heuristic(description, title)
        
        # Build article entry
        art_entry = {
            "article_number": art_num,
            "title": title,
            "part": part_name,
            "chapter": chapter_name,
            "full_text": description,
            "fundamental_right": "Right to Freedom" if part_name == "Part III - Fundamental Rights" else "",
            "constitutional_part": part_name.split("-")[0].strip() if "-" in part_name else part_name,
            "related_articles": [],
            "clauses": [
                {
                    "clause_id": f"art_{art_num}_child_0",
                    "clause": art_num,
                    "text": f"{title}: {description[:400]}..." if len(description) > 400 else f"{title}: {description}",
                    "category": category,
                    "keywords": kws,
                    "legal_topics": [title],
                    "related_cases": []
                }
            ]
        }
        processed_articles.append(art_entry)
        seen_art_nos.add(art_num)
        
    # 4. Add Schedules
    for sch in schedules:
        processed_articles.append(sch)
        
    # 5. Add Amendments
    for am in amendments:
        processed_articles.append(am)
        
    print(f"Total structured articles/schedules/amendments: {len(processed_articles)}")
    
    # Save the expanded constitution
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "constitution_articles.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(processed_articles, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated expanded constitution at {output_path}")

if __name__ == "__main__":
    main()
