# Ontology Description

We developed this ontology in order to use axioms to define chord degrees. We use concepts from the Chord Ontology, the Music Theory Ontology and the Tonality Ontology. We created our ontology using Owlready2 for python and a blank file named onto.owl. We created equivalent concepts for every concept defined on the ontologies we use.

# Prefixes
chord ontology -> chord
music theory ontology -> mto
tonality ontology -> to

# Object Properties

onto:hasNext (chord>>chord)
onto:hasPrevious (chord>>chord)
onto:hasKey (chord>>tonality)

# Data Properties

onto:hasBars (chord>>decimal)
onto:hasTimeSignature (chord>>integer)

# Classes

chord:Chord
to:Key
mto:Progression

# to:Key subclasses

onto:Key_A
onto:Key_Ab
...

# chord:Chord subclasses

onto:NoChord
onto:Root
onto:Degree
onto:ChordType
mto:Triad
mto:Tetrad

# onto:Root subclasses

onto:A_chord (all chords using A as their root note)
onto:Ab_chord (all chords using Ab as their root note)
...

# onto:ChordType subclasses

onto:MajorChord (all major chords)
onto:MinorChord (all minor chords)
onto:DiminishedChord ...
onto:HalfDiminishedChord ...
onto:AugmentedChord ...
onto:SuspendedChord ...

# onto:Degree subclasses

onto:First (first degree)
onto:FlatFirst (first degree)
...

# onto:Degree axioms example

\exists hasKey.Key_A \And E_chord \subseteq Fifth

