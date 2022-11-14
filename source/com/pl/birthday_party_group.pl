/* Facts */
student("Smith").
student("KG").
student("Rani").
student("Pinky").
student("Miny").
student("Ster").
student("Rocky").
student("Monu").
student("Boku").
student("Tina").

/* Group of Smith, KG, Rani */

friends("Smith","KG").
friends("KG","Smith").
friends("Rani","KG").
friends("KG","Rani").
friends("Smith","Rani").
friends("Rani","Smith").

/* Group of Rocky, Miny, Ster, Pinky */

friends("Rocky","Miny").
friends("Rocky","Ster").
friends("Rocky","Pinky").
friends("Ster","Pinky").
friends("Ster","Miny").
friends("Ster","Rocky").
friends("Miny","Pinky").
friends("Miny","Ster").
friends("Miny","Rocky").
friends("Pinky","Ster").
friends("Pinky","Miny").
friends("Pinky","Rocky").

/* Group of Monu, Boku, Tina */

friends("Monu","Boku").
friends("Monu","Tina").
friends("Tina","Boku").
friends("Tina","Monu").
friends("Boku","Tina").
friends("Boku","Monu").

parent("Smith", "Father of Smith", "Mother of Smith").
parent("KG", "Father of KG", "Mother of KG").
parent("Rani", "Father of Rani", "Mother of Rani").
parent("Pinky", "Father of Pinky", "Mother of Pinky").
parent("Miny", "Father of Miny", "Mother of Miny").
parent("Ster", "Father of Ster", "Mother of Ster").
parent("Rocky", "Father of Rocky", "Mother of Rocky").
parent("Monu", "Father of Monu", "Mother of Monu").
parent("Boku", "Father of Boku", "Mother of Boku").
parent("Tina", "Father of Tina", "Mother of Tina").

/* Rules */
group(X,Y):-
friends(X,Y),
friends(Y,X).
guestlist(X):-
write("Created the list");
group(X,Y),X\==Y,write(Y),
group(X,Y),X\==Y,parent(Y,Z,W),write(" " + Z),
group(X,Y),X\==Y,parent(Y,Z,W),write(" " + W + " ").