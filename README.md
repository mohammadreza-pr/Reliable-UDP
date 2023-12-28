# Reliable UDP

This project is done as part of the Computer Networks course at Sharif University Fall 2023.

My project was implementing a reliable protocol to transfer packets on the UDP. So, I implemented RDT 3.0 based on the stop-and-wait method. There are two sides: receiver and sender.

## Sender
- Listens on port 8050 localhost.
- Adds `ack` and `seq_number` headers to each packet received on port 8050.
- Sends it via a lossy link which I used from this repository: [lossy_link](https://github.com/HirbodBehnam/lossy_link).

## Behaviour on Packet Loss
- If a packet is lost, the sender will resend it after 0.75 seconds.

## Lossy Link
- Connects port 12345 to 54321 of localhost.
- Transfers data between the two sides but can lose packets or change the order.

## Receiver
- Listens on port 54321.
- Checks the `seq_number` of each packet.
  - If the `seq_number` is correct, it will send the packet to port 5080.
  - If it's not correct, it will send the right `ack_number` to the sender.

## Automata Images
The automata for the sender and receiver sides are provided by GeeksforGeeks, a comprehensive computer science resource:

- The automata of the sender side can be viewed here:
  ![Sender Automata](https://media.geeksforgeeks.org/wp-content/uploads/20220904072605/s1.png)

- The automata of the receiver side can be viewed here:
  ![Receiver Automata](https://media.geeksforgeeks.org/wp-content/uploads/20220818183806/s15.png)

Images sourced from www.geeksforgeeks.org.