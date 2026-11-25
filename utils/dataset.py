from model.document import Document
from model.query import Query



documents = [
    Document("D1", "cats sit on the mat. the cat has sharp claws, and it is very agile."),
    Document("D2", "dogs play in the garden. the dog loves a ball and is very playful."),
    Document("D3", "cats and dogs are friendly. dogs have soft tails."),
    Document("D4", "dogs chase balls outside. the puppies run across the yard."),
    Document("D5", "the garden has flowers and trees. bees fly between the plants."),

    Document("D6", "kittens sleep in a warm basket. the small cats enjoy soft blankets."),
    Document("D7", "a black cat climbs the wooden fence. it watches birds in the garden."),
    Document("D8", "the puppy plays with a red ball. its owner throws the ball across the yard."),
    Document("D9", "dogs enjoy long walks in the park. large dogs need regular exercise."),
    Document("D10", "a friendly puppy follows the children. the dog waits near the garden gate."),

    Document("D11", "roses grow beside the garden wall. the flowers need sunlight and water."),
    Document("D12", "tomato plants grow in the vegetable garden. gardeners pick fresh tomatoes."),
    Document("D13", "green trees provide shade in the playground. children sit beneath the branches."),
    Document("D14", "butterflies visit colorful flowers. they move gently across the garden."),
    Document("D15", "the gardener waters plants every morning. healthy flowers need enough water."),

    Document("D16", "birds build nests in tall trees. the young birds wait for food."),
    Document("D17", "small sparrows search for seeds near the garden path."),
    Document("D18", "a blue bird rests on the fence. it sings during the morning."),
    Document("D19", "ducks swim across the small pond. the water is calm and clean."),
    Document("D20", "rabbits hide under the bushes. they eat fresh grass from the garden."),

    Document("D21", "children read books inside the classroom. the teacher explains a new lesson."),
    Document("D22", "students write numbers on the board. mathematics practice starts after lunch."),
    Document("D23", "the teacher prepares an art activity. children use paper, paint, and brushes."),
    Document("D24", "students play together during break time. the playground is full of laughter."),
    Document("D25", "the classroom has colorful chairs and tables. every child keeps their books nearby."),

    Document("D26", "the school bus arrives early in the morning. children wait near the entrance."),
    Document("D27", "a driver checks the bus before departure. safety belts protect the children."),
    Document("D28", "parents collect their children after school. staff members check the pickup list."),
    Document("D29", "the kindergarten entrance is clean and bright. visitors wait at reception."),
    Document("D30", "teachers record attendance every morning. absent children are marked in the system."),

    Document("D31", "rain falls over the garden. the wet leaves shine beneath the cloudy sky."),
    Document("D32", "the sun is bright today. children wear hats when they play outside."),
    Document("D33", "strong wind moves the trees. outdoor activities are postponed during bad weather."),
    Document("D34", "a rainbow appears after the rain. children look at the colorful sky."),
    Document("D35", "the morning is cool and peaceful. birds sing near the school garden."),

    Document("D36", "healthy meals include vegetables and fruit. children drink water during lunch."),
    Document("D37", "the kitchen prepares fresh meals every day. staff check the food schedule."),
    Document("D38", "some children have food allergies. teachers review the allergy information."),
    Document("D39", "lunch is served at noon. every child has a labeled meal."),
    Document("D40", "the menu includes rice, chicken, and vegetables. parents can view the weekly menu."),

    Document("D41", "children wash their hands before eating. clean hands help prevent illness."),
    Document("D42", "the nurse checks a child who feels unwell. parents receive a health notification."),
    Document("D43", "the classroom has a quiet rest area. children sleep after lunch."),
    Document("D44", "teachers help children put on their coats. the weather is cold outside."),
    Document("D45", "a child is absent from kindergarten today. the teacher records the absence."),

    Document("D46", "parents receive daily updates on the mobile application. staff share photos and notes."),
    Document("D47", "the school sends a notification about tomorrow's activity."),
    Document("D48", "parents can message the teacher through the application."),
    Document("D49", "the kindergarten calendar shows upcoming events and holidays."),
    Document("D50", "staff review attendance, meals, transportation, and classroom activities every morning."),
]


queries = {
    "Q1": Query("Q1", "cats and kittens behavior"),
    "Q2": Query("Q2", "dogs playing with balls in the garden"),
    "Q3": Query("Q3", "garden flowers plants and water"),
    "Q4": Query("Q4", "birds and small animals in the garden"),
    "Q5": Query("Q5", "classroom teacher and learning activities"),
    "Q6": Query("Q6", "school bus safety pickup and attendance"),
    "Q7": Query("Q7", "weather conditions and outdoor activities"),
    "Q8": Query("Q8", "children meals lunch allergies and menu"),
    "Q9": Query("Q9", "child health rest and absence"),
    "Q10": Query("Q10", "parent mobile messages calendar and updates"),
    "Q11": Query("Q11", "quantum computing research"),
}


qrels = {
    "Q1": {
        "D1": 3,
        "D6": 2,
        "D7": 2,
        "D3": 1,
    },

    "Q2": {
        "D2": 3,
        "D4": 2,
        "D8": 2,
        "D9": 2,
        "D10": 1,
        "D3": 1,
    },

    "Q3": {
        "D5": 3,
        "D11": 3,
        "D12": 2,
        "D14": 2,
        "D15": 3,
        "D31": 1,
        "D35": 1,
    },

    "Q4": {
        "D16": 3,
        "D17": 3,
        "D18": 3,
        "D19": 2,
        "D20": 2,
        "D7": 1,
    },

    "Q5": {
        "D21": 3,
        "D22": 2,
        "D23": 3,
        "D24": 2,
        "D25": 2,
        "D13": 1,
    },

    "Q6": {
        "D26": 3,
        "D27": 3,
        "D28": 3,
        "D30": 2,
        "D50": 2,
        "D29": 1,
    },

    "Q7": {
        "D31": 3,
        "D32": 3,
        "D33": 3,
        "D34": 2,
        "D35": 2,
        "D44": 2,
    },

    "Q8": {
        "D36": 3,
        "D37": 2,
        "D38": 3,
        "D39": 3,
        "D40": 3,
        "D41": 1,
    },

    "Q9": {
        "D42": 3,
        "D45": 3,
        "D43": 2,
        "D41": 2,
        "D36": 1,
        "D38": 1,
    },

    "Q10": {
        "D46": 3,
        "D47": 2,
        "D48": 3,
        "D49": 2,
        "D50": 1,
    },

    # Intentional has no relevance judgments.
    "Q11": {},
}


# Retrieval output: query ID → ranked document IDs
baseline_runs = {
    "Q1": ["D2", "D1", "D3"],
    "Q2": ["D4", "D2", "D5"],
    "Q3": ["D1"],
}

# candidate output: query ID → ranked document IDs
candidate_runs = {
    "Q1": ["D2", "D1", "D3"],
    # "Q2": ["D2", "D4", "D5"],
    "Q2": ["D4", "D5", "D2"],
    "Q3": ["D1"],
}

