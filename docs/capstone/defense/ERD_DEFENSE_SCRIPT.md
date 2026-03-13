# ERD Defense Script: Entity Discussion (Layout-Based)

**Concept:** A team member walks the panel through the ERD **from Left to Right**, following the diagram's visual flow.

---

## 1. Column 1: The User Entity (The Actor)

**Discussion by Team Member:**

"Simulan po natin sa pinaka-kaliwa, ang **Column 1**, which acts as the entry point of our system."

*   **Purpose:**
    "So bale sa `User` entity, ang pinaka-purpose po nito is to manage identity at access control. May tatlong klase po ng user dito: regular tourists, content contributors, at system administrators."

*   **Significance of Attributes:**
    "So sa **Significance of Attributes:** naman po, yung `username` at `email` po yung unique identifiers to prevent duplicate accounts.
    *   Yung `password_hash` naman po is para ma-store yung passwords nang secure, encrypted po siya para safety.
    *   Sa `role` naman po, dito dines-define kung admin ka, contributor, or user ka lang. Ito po yung nagkokontrol ng access.
    *   Yung `is_approved` naman po is parang verification, lalo na sa contributors bago sila makapag-post ng heritage data."

*   **Nature of Relationships:**
    "So yung `User` entity po halos naka-connect po siya sa lahat in a **'Parent-Child'** manner.
    *   One User can create *many* Attractions (Parent to many Children).
    *   One User can write *many* Reviews.
    *   This relationship allows us to track *ownership*—laging alam ng system kung sino ang gumawa ng record at kung sino ang responsible for it."

---

## 2. Column 2: Tourism Content (The Public Face)

"Next po, sa **Column 2**, makikita natin ang mga main content na pang-turista."

### A. The Attraction Entity

*   **Purpose:**
    "Ito po yung `Attraction` entity. So bale ito po yung 'Tourist Brochure' version ng data natin. Kung yung Heritage Profile is pang-research, ito naman po is para sa mga turista—simplified at madaling intindihin."

*   **Significance of Attributes:**
    "Focus po dito is location at display.
    *   Yung `lat` at `lng` (Latitude/Longitude) naman po, ito yung coordinates para lumabas siya nang tama sa interactive map.
    *   Yung `category` po (Nature, Adventure, Religious), ginagamit 'to para ma-filter ng turista kung ano gusto nilang puntahan.
    *   Yung `image_url` naman po, ito yung picture na makikita sa app."

*   **Nature of Relationships:**
    "Sa relationship po, direkta siyang ka-partner ng `HeritageProfile` (**One-to-One**).
    *   Ibig sabihin, kapag may Heritage Profile na na-approve, automatic magkakaroon din siya ng Attraction card para sa turista."

### B. The Event Entity

*   **Purpose:**
    "Sunod naman po ang `Event` entity. Ito yung nagha-handle ng timeline o mga ganap sa Mangatarem, like festivals at fiestas. Hindi lang kasi places ang mahalaga, pati yung activities."

*   **Significance of Attributes:**
    "Time po ang pinaka-importante dito.
    *   Yung `date` po, para ma-sort natin kung 'Upcoming' pa lang or tapos na yung event.
    *   Yung `category` naman po, kung Religious ba or Civic event, para makapili yung turista.
    *   Sa `status` naman po, para sure tayo na verified at official events lang ang lumalabas sa calendar."

*   **Nature of Relationships:**
    "Sa interaction naman po, connected siya sa Users via **'Interest List'**.
    *   Maraming user ang pwedeng maging interested sa isang event.
    *   Parang popularity counter po siya, para makita natin kung alin ang trending."

### C. Barangay Info Entity

*   **Purpose:**
    "Makikita rin dito ang `BarangayInfo`. Ito yung identity ng bawat barangay. May 82 barangays po tayo sa Mangatarem, so dito nakalagay yung history at kwento ng bawat isa."

*   **Significance of Attributes:**
    "Puro kwento po ang attributes dito.
    *   Yung `history` at `local_practices` po, dito nakasulat yung unique story ng community.
    *   Yung `barangay_name` po, ito yung label o tag. Ginagamit natin 'to para malaman kung saang barangay nakapwesto ang isang attraction."

*   **Nature of Relationships:**
    "Bale **Reference Entity** lang po siya.
    *   Pwede tayong gumawa ng 'Barangay Profile' page kung saan, pag-click mo ng isang barangay (example: Poblacion), makikita mo lahat ng tourist spots na under sa kanya."

---

## 3. Column 3: Heritage Framework (The Cultural Core)

"Sa gitna po, sa **Column 3**, nandito ang puso ng system—ang Heritage Data."

### The Heritage Profile Entity

*   **Purpose:**
    "So bale sa `HeritageProfile` naman po, ito yung pinaka-repository ng cultural data natin. Ang purpose po nito is para ma-standardize yung pag-document natin ng heritage—mapa-bahay man yan o kwento—sinisigurado natin na pasok siya sa standards ng cultural mapping."

*   **Significance of Attributes:**
    "Yung mga attributes naman po dito, mas detalyado kumpara sa simpleng tourism data.
    *   Yung `form_control_number` naman po, ito yung parang link natin o 'digital twin' ng physical paper forms na ginagamit sa manual mapping.
    *   Sa `significance`, `conservation_measures`, at `key_informants`, dito nakalagay yung kwento at halaga ng lugar para sa preservation.
    *   Yung `status` naman po, dito makikita kung 'draft' pa lang ba yung data or kung 'published' na."

*   **Nature of Relationships:**
    "Sa relationship naman po, **'One-to-One Polymorphic'** siya.
    *   Parang ganito po: May isang generic form tayo na `HeritageProfile` (yung general details), tapos naka-link siya sa specific form depende kung ano siya.
    *   Kung bahay siya, connect siya sa `BuiltHeritage`. Kung ilog naman, connect siya sa `NaturalHeritage`.
    *   Ginawa po natin 'to para organized at hindi magulo yung database natin."

---

## 4. Column 4: Interaction & Engagement (The User Voice)

"Lastly po, sa pinaka-kanan o **Column 4**, nandito ang interaction tables: `Review`, `Favorite`, `EventInterest`, at `PageView`."

*   **Purpose:**
    "Ang purpose po nito is para maging interactive yung system—hindi lang siya basta nagbabasa, nakaka-engage din yung user at may boses sila."

*   **Significance of Attributes:**
    "Attributes po dito measure satisfaction.
    *   Yung `rating` po (1-5 stars), para ma-rank natin kung alin ang best places.
    *   Yung `comment` naman po, feedback ng user kung nag-enjoy ba sila.
    *   Yung `timestamp` po sa `PageView`, para malaman natin kung alin ang most-viewed attractions."

*   **Nature of Relationships:**
    "Bale **'Connectors'** lang po sila sa gitna.
    *   Link lang po siya between User at Attraction.
    *   Example po sa `Favorite`, sinasabi lang nito na 'Gusto ni User A itong Attraction B'. Dahil dito, nakakagawa tayo ng personalized 'Saved Places' list para sa bawat turista."

---
