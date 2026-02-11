const locationData = {
    "Andhra Pradesh": {
        "Anantapur": ["Anantapur", "Dharmavaram", "Hindupur", "Gooty", "Tadipatri"],
        "Chittoor": ["Chittoor", "Tirupati", "Madanapalle", "Srikalahasti", "Palamaner"],
        "East Godavari": ["Kakinada", "Rajahmundry", "Amalapuram", "Peddapuram"],
        "Guntur": ["Guntur", "Tenali", "Narasaraopet", "Bapatla"],
        "Krishna": ["Machilipatnam", "Vijayawada", "Gudivada", "Nuzvid"],
        "Kurnool": ["Kurnool", "Nandyal", "Adoni", "Dhone"],
        "Prakasam": ["Ongole", "Kandukur", "Markapur"],
        "Sri Potti Sriramulu Nellore": ["Nellore", "Gudur", "Kavali", "Atmakur"],
        "Srikakulam": ["Srikakulam", "Tekkali", "Palakonda"],
        "Visakhapatnam": ["Visakhapatnam", "Anakapalle", "Narsipatnam"],
        "Vizianagaram": ["Vizianagaram", "Parvathipuram", "Bobbili"],
        "West Godavari": ["Eluru", "Bhimavaram", "Tadepalligudem", "Narsapuram"],
        "YSR Kadapa": ["Kadapa", "Jammalamadugu", "Proddatur", "Rajampet"]
    },
    "Arunachal Pradesh": {
        "Tawang": ["Tawang", "Lumla"],
        "West Kameng": ["Bomdila", "Dirang"],
        "East Kameng": ["Seppa", "Chayang Tajo"],
        "Papum Pare": ["Itanagar", "Naharlagun", "Doimukh"]
    },
    "Assam": {
        "Baksa": ["Mushalpur", "Tamulpur"],
        "Barpeta": ["Barpeta", "Bajali"],
        "Biswanath": ["Biswanath Chariali", "Gohpur"],
        "Bongaigaon": ["Bongaigaon", "Bijni"],
        "Cachar": ["Silchar", "Lakhipur"],
        "Dibrugarh": ["Dibrugarh", "Moran"],
        "Guwahati": ["Dispur", "Guwahati"],
        "Jorhat": ["Jorhat", "Titabor"],
        "Kamrup": ["Rangia", "Hajo"],
        "Nagaon": ["Nagaon", "Kaliabor"]
    },
    "Bihar": {
        "Patna": ["Patna Sadar", "Danapur", "Barh", "Masaurhi"],
        "Gaya": ["Gaya Sadar", "Tekari", "Sherghati"],
        "Bhagalpur": ["Bhagalpur", "Kahalgaon", "Naugachia"],
        "Muzaffarpur": ["Muzaffarpur East", "Muzaffarpur West"],
        "Darbhanga": ["Darbhanga", "Benipur", "Biraul"]
    },
    "Chhattisgarh": {
        "Raipur": ["Raipur", "Arang", "Abhanpur"],
        "Bilaspur": ["Bilaspur", "Kota", "Takhatpur"],
        "Durg": ["Durg", "Bhilai", "Patan"]
    },
    "Delhi": {
        "Central Delhi": ["Daryaganj", "Pahar Ganj", "Karol Bagh"],
        "East Delhi": ["Gandhi Nagar", "Preet Vihar", "Mayur Vihar"],
        "New Delhi": ["Connaught Place", "Parliament Street", "Chanakyapuri"],
        "North Delhi": ["Sadar Bazar", "Kotwali", "Civil Lines"],
        "North East Delhi": ["Seelampur", "Yamuna Vihar", "Karawal Nagar"],
        "North West Delhi": ["Saraswati Vihar", "Rohini", "Kanjhawala"],
        "South Delhi": ["Saket", "Hauz Khas", "Mehrauli"],
        "South West Delhi": ["Dwarka", "Najafgarh", "Kapashera"],
        "West Delhi": ["Patel Nagar", "Rajouri Garden", "Punjabi Bagh"]
    },
    "Goa": {
        "North Goa": ["Bardez", "Bicholim", "Pernem", "Ponda", "Sattari", "Tiswadi"],
        "South Goa": ["Canacona", "Mormugao", "Salcete", "Sanguem", "Quepem", "Dharbandora"]
    },
    "Gujarat": {
        "Ahmedabad": ["Ahmedabad City", "Daskroi", "Sanand"],
        "Surat": ["Surat City", "Choryasi", "Olpad"],
        "Vadodara": ["Vadodara City", "Padra", "Karjan"],
        "Rajkot": ["Rajkot", "Gondal", "Jetpur"]
    },
    "Haryana": {
        "Gurugram": ["Gurugram", "Sohna", "Pataudi"],
        "Faridabad": ["Faridabad", "Ballabgarh"],
        "Panipat": ["Panipat", "Samalkha"],
        "Ambala": ["Ambala", "Barara", "Naraingarh"]
    },
    "Himachal Pradesh": {
        "Shimla": ["Shimla", "Theog", "Rampur"],
        "Kangra": ["Dharamshala", "Kangra", "Palampur"],
        "Mandi": ["Mandi", "Sundernagar"]
    },
    "Jharkhand": {
        "Ranchi": ["Ranchi", "Bundu"],
        "Dhanbad": ["Dhanbad", "Jharia"],
        "Jamshedpur": ["Golmuri", "Patamda"]
    },
    "Karnataka": {
        "Bagalkot": ["Bagalkot", "Badami", "Hungund", "Jamkhandi", "Mudhol"],
        "Bangalore Rural": ["Devanahalli", "Doddaballapura", "Hosakote", "Nelamangala"],
        "Bangalore Urban": ["Bangalore North", "Bangalore South", "Bangalore East", "Anekal", "Yelahanka"],
        "Belagavi": ["Belagavi", "Gokak", "Chikkodi", "Athani", "Bailhongal"],
        "Bellary": ["Bellary", "Sandur", "Siruguppa"],
        "Bidar": ["Bidar", "Basavakalyan", "Bhalki", "Humnabad"],
        "Chamarajanagar": ["Chamarajanagar", "Gundlupet", "Kollegal"],
        "Chikkaballapur": ["Chikkaballapur", "Chintamani", "Gauribidanur"],
        "Chikkamagaluru": ["Chikkamagaluru", "Kadur", "Tarikere", "Mudigere"],
        "Chitradurga": ["Chitradurga", "Hiriyur", "Challakere"],
        "Dakshina Kannada": ["Mangalore", "Bantwal", "Puttur", "Belthangady", "Sullia"],
        "Davanagere": ["Davanagere", "Harihar", "Jagalur"],
        "Dharwad": ["Dharwad", "Hubli", "Kalghatgi"],
        "Gadag": ["Gadag", "Ron", "Shirhatti"],
        "Hassan": ["Hassan", "Arsikere", "Channarayapatna"],
        "Haveri": ["Haveri", "Ranebennur", "Byadgi"],
        "Kalaburagi": ["Kalaburagi", "Aland", "Afzalpur"],
        "Kodagu": ["Madikeri", "Somwarpet", "Virajpet"],
        "Kolar": ["Kolar", "Bangarapet", "Malur"],
        "Koppal": ["Koppal", "Gangavathi", "Kushtagi"],
        "Mandya": ["Mandya", "Maddur", "Malavalli"],
        "Mysore": ["Mysore", "Hunsur", "Nanjangud", "Periyapatna", "T.Narsipur"],
        "Raichur": ["Raichur", "Manvi", "Sindhanur"],
        "Ramanagara": ["Ramanagara", "Channapatna", "Kanakapura", "Magadi"],
        "Shivamogga": ["Shivamogga", "Bhadravathi", "Sagar", "Shikaripura"],
        "Tumakuru": ["Tumakuru", "Gubbi", "Kunigal", "Tiptur"],
        "Udupi": ["Udupi", "Kundapura", "Karkala"],
        "Uttara Kannada": ["Karwar", "Sirsi", "Bhatkal", "Kumta"],
        "Vijayapura": ["Vijayapura", "Indi", "Sindgi"],
        "Yadgir": ["Yadgir", "Shahapur", "Shorapur"]
    },
    "Kerala": {
        "Alappuzha": ["Alappuzha", "Chengannur", "Cherthala", "Karthikappally", "Kuttanad", "Mavelikkara"],
        "Ernakulam": ["Aluva", "Kanayannur", "Kochi", "Kothamangalam", "Kunnathunad", "Muvattupuzha", "Paravur"],
        "Idukki": ["Devikulam", "Idukki", "Peerumade", "Thodupuzha", "Udumbanchola"],
        "Kannur": ["Kannur", "Taliparamba", "Thalassery", "Iritty", "Payyanur"],
        "Kasaragod": ["Hosdurg", "Kasaragod", "Manjeshwaram", "Vellarikundu"],
        "Kollam": ["Kollam", "Karunagappally", "Kunnathur", "Kottarakkara", "Punalur", "Pathanapuram"],
        "Kottayam": ["Changanassery", "Kanjirappally", "Kottayam", "Meenachil", "Vaikom"],
        "Kozhikode": ["Kozhikode", "Quilandy", "Thamarassery", "Vadakara"],
        "Malappuram": ["Ernad", "Nilambur", "Perinthalmanna", "Ponnani", "Tirur", "Tirurangadi", "Kondotty"],
        "Palakkad": ["Alathur", "Chittur", "Mannarkkad", "Ottappalam", "Palakkad", "Pattambi"],
        "Pathanamthitta": ["Adoor", "Konni", "Kozhencherry", "Mallappally", "Ranni", "Thiruvalla"],
        "Thiruvananthapuram": ["Thiruvananthapuram", "Chirayinkeezhu", "Nedumangad", "Neyyattinkara", "Varkala", "Kattakada"],
        "Thrissur": ["Chalakudy", "Chavakkad", "Kodungallur", "Mukundapuram", "Talappilly", "Thrissur"],
        "Wayanad": ["Mananthavady", "Sulthan Bathery", "Vythiri"]
    },
    "Madhya Pradesh": {
        "Bhopal": ["Huzur", "Berasia"],
        "Indore": ["Indore", "Mhow", "Sanwer"],
        "Gwalior": ["Gwalior", "Dabra"],
        "Jabalpur": ["Jabalpur", "Sihora"]
    },
    "Maharashtra": {
        "Mumbai City": ["Colaba", "Dadar", "Sion", "Fort"],
        "Mumbai Suburban": ["Andheri", "Borivali", "Kurla", "Bandra"],
        "Pune": ["Pune City", "Haveli", "Mulshi", "Maval", "Baramati", "Junnar"],
        "Nagpur": ["Nagpur City", "Nagpur Rural", "Kamptee", "Hingna"],
        "Thane": ["Thane", "Kalyan", "Ulhasnagar", "Bhiwandi", "Ambernath"],
        "Nashik": ["Nashik", "Malegaon", "Niphad", "Sinnar"],
        "Aurangabad": ["Aurangabad", "Paithan", "Gangapur"],
        "Solapur": ["Solapur North", "Solapur South", "Barshi"],
        "Kolhapur": ["Karvir", "Panhala", "Hatkanangale"]
    },
    "Odisha": {
        "Bhubaneswar": ["Bhubaneswar"],
        "Cuttack": ["Cuttack Sadar", "Athagarh"],
        "Puri": ["Puri", "Konark"]
    },
    "Punjab": {
        "Amritsar": ["Amritsar-I", "Amritsar-II", "Ajnala"],
        "Ludhiana": ["Ludhiana East", "Ludhiana West", "Jagraon"],
        "Jalandhar": ["Jalandhar-I", "Jalandhar-II", "Phillaur"]
    },
    "Rajasthan": {
        "Jaipur": ["Jaipur", "Sanganer", "Amber"],
        "Jodhpur": ["Jodhpur", "Luni", "Bilara"],
        "Udaipur": ["Girwa", "Mavli", "Vallabhnagar"]
    },
    "Tamil Nadu": {
        "Chennai": ["Egmore", "Guindy", "Mambalam", "Mylapore", "Perambur", "Tondiarpet", "Velachery", "Purasawalkam"],
        "Coimbatore": ["Coimbatore North", "Coimbatore South", "Pollachi", "Mettupalayam", "Sulur", "Valparai"],
        "Madurai": ["Madurai North", "Madurai South", "Melur", "Thirumangalam", "Usilampatti", "Vadipatti"],
        "Kancheepuram": ["Kancheepuram", "Sriperumbudur", "Uthiramerur", "Walajabad"],
        "Tiruvallur": ["Tiruvallur", "Poonamallee", "Avadi", "Ponneri"],
        "Salem": ["Salem", "Attur", "Mettur", "Omalur", "Sankari"],
        "Tiruchirappalli": ["Tiruchirappalli", "Srirangam", "Manapparai", "Thuraiyur"],
        "Tirunelveli": ["Tirunelveli", "Palayamkottai", "Ambasamudram", "Nanguneri"],
        "Erode": ["Erode", "Bhavani", "Gobichettipalayam", "Perundurai", "Sathyamangalam"],
        "Vellore": ["Vellore", "Katpadi", "Gudiyatham", "Anaicut"]
    },
    "Telangana": {
        "Hyderabad": ["Hyderabad", "Secunderabad", "Musheerabad", "Charminar"],
        "Ranga Reddy": ["Shamshabad", "Rajendranagar", "Serilingampally"],
        "Medchal-Malkajgiri": ["Malkajgiri", "Kukatpally", "Uppal"],
        "Warangal": ["Warangal", "Khila Warangal"]
    },
    "Uttar Pradesh": {
        "Lucknow": ["Lucknow", "Malihabad", "Mohanlalganj"],
        "Kanpur Nagar": ["Kanpur", "Bilhaur"],
        "Ghaziabad": ["Ghaziabad", "Modinagar", "Loni"],
        "Gautam Buddha Nagar": ["Noida", "Dadri", "Jewar"],
        "Varanasi": ["Varanasi", "Pindra", "Raja Talab"],
        "Agra": ["Agra", "Etmadpur", "Kheragarh"]
    },
    "West Bengal": {
        "Kolkata": ["Kolkata"],
        "North 24 Parganas": ["Barasat", "Barrackpore", "Bongaon"],
        "South 24 Parganas": ["Alipore", "Baruipur", "Canning"],
        "Howrah": ["Howrah", "Uluberia"],
        "Darjeeling": ["Darjeeling", "Kurseong", "Siliguri"]
    }
};