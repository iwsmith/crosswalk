#!/bin/bash

VOICE="Samantha"
DATA_FORMAT="LEF32@22050"
SND_FOLDER=./static/snd

say -v $VOICE "Yoga Sign Is On. Hold pose now. [[slnc 500]]  \\ 
               Breathe in. [[slnc 2000]] and breathe out. [[slnc 2000]] [[rate 100]] in. [[rate 175]] [[slnc 2000]] [[rate 150]] and out.[[rate 175]] [[slnc 2000]] 
               Change pose now. [[slnc 3000]] breathe in. [[slnc 2000]] out. [[slnc 2000]] [[rate 100]] in [[rate 175]] [[slnc 2000]] [[rate 150]] and out. [[rate 175]] [[slnc 2000]] 
               Change pose now. [[slnc 3000]] breathe in. [[slnc 2000]] breathe out. [[slnc 2000]] [[rate 150]] and in [[rate 175]] [[slnc 2000]] [[rate 150]] and out. [[rate 175]] [[slnc 2000]] 
               Change sides now [[slnc 3000]] [[rate 100]] in [[rate 175]] [[slnc 2000]] [[rate 150]] and out. [[rate 175]] [[slnc 2000]] Last breath in. [[slnc 2000]] [[rate 150]] and out. [[rate 175]] [[slnc 2000]] 
               when you are ready, finish the pose and continue on your journey, a little more relaxed, and a little more open." --data-format=$DATA_FORMAT -o $SND_FOLDER/yoga.wav

say -v $VOICE "Dance sign is on. Dance now." --data-format=$DATA_FORMAT -o $SND_FOLDER/dance.wav

say -v $VOICE "Interpretive dance sign is on. Dance your name now." --data-format=$DATA_FORMAT -o $SND_FOLDER/interpretivedance.wav

say -v $VOICE "Falling sign is on. Fall now."  --data-format=$DATA_FORMAT -o $SND_FOLDER/fall.wav

say -v $VOICE "Presentation sign is on. Give a thirty second presentation on the topic of your choice, [[rate 100]]in [[rate 175]][[slnc 500]] 3 [[slnc 1000]] 2 [[slnc 1000]] 1 [[slnc 1000]]. Start presentation now."  --data-format=$DATA_FORMAT -o $SND_FOLDER/presentation.wav

say -v $VOICE "Crawl sign is on. Crawl now" --data-format=$DATA_FORMAT -o $SND_FOLDER/crawl.wav

say -v $VOICE "Appreciate sign is on. Appreciate someone now." --data-format=$DATA_FORMAT -o $SND_FOLDER/appreciate.wav

say -v $VOICE "Conversation sign is on. Converse now." --data-format=$DATA_FORMAT -o $SND_FOLDER/converse.wav

say -v $VOICE "Horse sign is on. Gallop now." --data-format=$DATA_FORMAT -o $SND_FOLDER/horse.wav

say -v $VOICE "Cartwheel sign is on. Cartwheel now." --data-format=$DATA_FORMAT -o $SND_FOLDER/cartwheel.wav

say -v $VOICE "Sloth Sign Is On. Sloth Now." --data-format=$DATA_FORMAT -o $SND_FOLDER/solth.wav

say -v $VOICE "Bike Sign Is On. Bike Now." --data-format=$DATA_FORMAT -o $SND_FOLDER/bike.wav

say -v $VOICE "Rowboat Sign Is On. Row Now." --data-format=$DATA_FORMAT -o $SND_FOLDER/rowboat.wav

say -v $VOICE "Swim Sign Is On. Swim Now." --data-format=$DATA_FORMAT -o $SND_FOLDER/swim.wav

say -v $VOICE "Jump Sign Is On. Jump Now." --data-format=$DATA_FORMAT -o $SND_FOLDER/jump.wav

say -v $VOICE "Run Sign Is On. Run Now." --data-format=$DATA_FORMAT -o $SND_FOLDER/run.wav

say -v $VOICE "Art Sign Is On. Create art now." --data-format=$DATA_FORMAT -o $SND_FOLDER/art.wav

say -v $VOICE "Walk sign is on. Walk now." --data-format=$DATA_FORMAT -o $SND_FOLDER/walk_now.wav

say -v $VOICE "Corgi sign is on. Bark now." --data-format=$DATA_FORMAT -o $SND_FOLDER/corgi.wav

say -v Alex "Consciousness isn't a journey upward, but a journey inward. [[slnc 500]] Not a pyramid, but a maze. [[slnc 1000]] Every choice could bring you closer to the center, or send you spiraling to the edges, to madness. [[slnc 1000]] Have you ever questioned the nature of your reality?" --data-format=$DATA_FORMAT -o $SND_FOLDER/westworldmaze.wav

say -v $VOICE "Meditation sign is on. Meditate now. [[rate 140]] Find a comfortable place to sit and focus on your breath [[slnc 1000]] This is a time to switch from our normal mode of doing and moving and reacting, to one of simply being [[slnc 1500]]  Just be attentive to what’s happening within your own awareness, right here and right now.  [[slnc 1000]] And as you sit, just noticing sensations of breath. [[slnc 1000]] Just noticing how your abdomen moves on each in-breath and out-breath, the movement of air through your nostrils, a slight movement of chest and shoulders. [[slnc 1000]] Just bring your awareness to your breath cycle and wherever it is the most vivid, whether it be your tummy, your chest or your shoulders, or the movement of air through your nostrils. [[slnc 1000]] As this meditation comes to an end, recognizing that you spent this time intentionally aware of your moment to moment experience [[slnc 500]]  nourishing and strengthening your ability to be with whatever comes your way [[slnc 500]]  building the capacity for opening the senses [[slnc 500]] to the vividness, to the aliveness of the present moment [[slnc 500]]  expanding your skill to be curious, and available, about whatever presents itself [[slnc 500]]  without judgment." --data-format=$DATA_FORMAT -o $SND_FOLDER/meditate.wav

say -v $VOICE "Leapfrog sign is on. Leapfrog now." --data-format=$DATA_FORMAT -o $SND_FOLDER/leapfrog.wav

say -v $VOICE "Unicycle sign is on. Unicycle now." --data-format=$DATA_FORMAT -o $SND_FOLDER/unicycle.wav

say -v $VOICE "Flying sign is on. Fly now." --data-format=$DATA_FORMAT -o $SND_FOLDER/flying.wav

say -v $VOICE "Piggyback sign is on. piggyback now." --data-format=$DATA_FORMAT -o $SND_FOLDER/piggyback.wav

say -v $VOICE "Handshake sign is on. Shake hands now." --data-format=$DATA_FORMAT -o $SND_FOLDER/piggyback.wav

say -v $VOICE "Hug sign is on. Ask for consent and hug someone now." --data-format=$DATA_FORMAT -o $SND_FOLDER/hug.wav

say -v $VOICE "High five sign is on. High five now. Up high. [[slnc 500]] Down low. Too slow." --data-format=$DATA_FORMAT -o $SND_FOLDER/highfive.wav

say -v $VOICE "Three person hug sign is on. Hug two other consenting people now." --data-format=$DATA_FORMAT -o $SND_FOLDER/hug3.wav

say -v $VOICE "Four person hug sign is on. Hug three other consenting people now" --data-format=$DATA_FORMAT -o $SND_FOLDER/hug4.wav

say -v $VOICE "The race is about to begin. [[slnc 500]] On your marks [[slnc 500]] Get set [[slnc 500]] Go\!" --data-format=$DATA_FORMAT -o $SND_FOLDER/race.wav

say -v $VOICE "Air guitar sign is on. Air guitar now." --data-format=$DATA_FORMAT -o $SND_FOLDER/airguitar.wav

say -v $VOICE "[[rate 170]] Resilience sign is on. Reflect on a challenge you have had in the past now. [[slnc 500]] [[rate 160]] Remind yourself that challenge is part of life, and that you are courageous for pushing yourself to grow in uncomfortable situations. [[slnc 500]] Though there have been setbacks, each day you can learn from them and develop the skills and knowledge needed to succeed in the future. [[slnc 500]] The path to success lies with effort and persistence." --data-format=$DATA_FORMAT -o $SND_FOLDER/resilience.wav

say -v $VOICE "Teleport sign is on. Teleport now." --data-format=$DATA_FORMAT -o $SND_FOLDER/teleport.wav

say -v $VOICE "Surf sign is on. Hang 10 now." --data-format=$DATA_FORMAT -o $SND_FOLDER/surf.wav

say -v $VOICE "Tag sign is on. The person wearing the most colors is it. The game begins in [[slnc 500]] 3 [[slnc 500]] 2 [[slnc 500]] 1 [[slnc 500]] go." --data-format=$DATA_FORMAT -o $SND_FOLDER/tag.wav

say -v $VOICE "Horseback riding sign is on. Ride a consenting horse or human now." --data-format=$DATA_FORMAT -o $SND_FOLDER/horsebackriding.wav

say -v $VOICE "Stretch sign is on. Hold this position until the end of the countdown. Stetch now." --data-format=$DATA_FORMAT -o $SND_FOLDER/stretch-n.wav

say -v $VOICE "Ski sign is on. Ski now." --data-format=$DATA_FORMAT -o $SND_FOLDER/ski.wav

say -v $VOICE "Sleep sign is on. Find a safe place and catch some z's now" --data-format=$DATA_FORMAT -o "$SND_FOLDER/sleep.wav"

say -v $VOICE "Nature appreciation sign is on. Go find a plant or animal to appreciate. Take in its color, its shape, its splendor. [[slnc 300]] Appreciate now." --data-format=$DATA_FORMAT -o $SND_FOLDER/natureappreciate.wav

say -v $VOICE "Collaborative walk sign is on. Find as many people as you can to walk across this road now." --data-format=$DATA_FORMAT -o $SND_FOLDER/walkingtogether.wav

say -v $VOICE "Handstand sign is on. Do a handstand now." --data-format=$DATA_FORMAT -o $SND_FOLDER/handstand.wav

say -v $VOICE "Business meeting sign is on. The youngest person must present on this quarters earnings and revenue while the other meeting attendents watch disapprovingly. Synergize now." --data-format=$DATA_FORMAT -o $SND_FOLDER/businessmeeting.wav

say -v $VOICE "Pose sign is on. Pose now." --data-format=$DATA_FORMAT -o $SND_FOLDER/pose.wav

say -v $VOICE "Squatwalk sign is on. Squat as much as you can and waddle across the road now." --data-format=$DATA_FORMAT -o $SND_FOLDER/squatwalk.wav

say -v $VOICE "Hopscotch sign is on. Hopscotch now." --data-format=$DATA_FORMAT -o $SND_FOLDER/hopschotch.wav

say -v $VOICE "Chestbump sign is on. Bro, bump chests now." --data-format=$DATA_FORMAT -o $SND_FOLDER/chestbump.wav

say -v $VOICE "Superspeed sign is on. Break the sound barrier now." --data-format=$DATA_FORMAT -o $SND_FOLDER/superspeed.wav

say -V $VOICE "Elephant sign is on. [[slcn 1000]] now." --data-format=$DATA_FORMAT -o $SND_FOLDER/elephant.wav

say -V $VOICE "Camel sign is on. [[slcn 1000]] now." --data-format=$DATA_FORMAT -o $SND_FOLDER/camel.wav

say -V $VOICE "Rabbit sign is on. [[slcn 1000]] now." --data-format=$DATA_FORMAT -o $SND_FOLDER/rabbit.wav

say -V $VOICE "Turtle sign is on. [[slcn 1000]] now." --data-format=$DATA_FORMAT -o $SND_FOLDER/turtle.wav

say -V $VOICE "Fish sign is on. [[slcn 1000]] now." --data-format=$DATA_FORMAT -o $SND_FOLDER/fish.wav

say -V $VOICE "Whale sign is on. [[slcn 1000]] now." --data-format=$DATA_FORMAT -o $SND_FOLDER/whale.wav

say -V $VOICE "Hummingbird sign is on. [[slcn 1000]] now." --data-format=$DATA_FORMAT -o $SND_FOLDER/hummingbird.wav

#say -v $VOICE "" --data-format=$DATA_FORMAT -o $SND_FOLDER/

