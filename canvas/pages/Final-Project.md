**The final project is for you!**

* Please think of what is interesting to you! What would you like to spend time on? What would you like to learn more about?
* What would be a good career starter for you? Startup business? Useful tool?
* Or maybe what sort of cool project would you like on your resume?

**Your final project could make the world a better place!**

* This is your chance to choose what you do with your time! Maybe you could solve a real problem or need with this time.
* Investing honest hard work into your own education makes the world a better place. Investment in you can be a blessing to everyone else.

**Collaboration!**

* This can be a chance to practice working with others, communicating your ideas, and listening to others.
* Please count on getting support, ideas, encouragement, reviews from peers, TAs, and the instructor.
* Feel free to form groups and work together.
* Everyone will get to share progress and issues you are facing with classmates during class.

**Required:**

* Requires reads and writes to some data. (Periodic data ingestion works for "writes"). We've learned about stateful systems and this is your chance to build one.
* Something about it that is interesting to you!
* Something that requires effort (**at least 30 to 40 hours**). If your initial project is very little work, that is fine. But if you spend 8 hours and are done, just create an additional project! Repeat until you fill the time.
* Something worthy of your resume, personal github, or career.

**Ideas to consider:**

* Security. Let's not hand out customer data to the world due to lack of security.
* Concurrency. Does this support multiple users making updates at the same time?
* Improving the world? Let's make the world a better place and leave it better than we found it.
* Uptime, availability, failover strategy, SLAs. Can you make this a reliable service even in the face of disasters and failures in a datacenter.

**More ideas to consider:**

* Profitable? Valuable to someone?
* Interface with external data
* Support 5000 writes per second (high scale)
* Support 5000 reads per second (high scale)
* Be for real customers
* Caching layer non-persistent (e.g. Redis) and persistent layer (e.g. Postgres SQL). Pick one of these strategies or come up with your own: cache-aside, query caching, write-behind, write-through, or cache prefetching. (See [https://redis.com/wp-content/uploads/2023/04/redis-enterprise-for-caching.pdf)Links to an external site.](https://redis.com/wp-content/uploads/2023/04/redis-enterprise-for-caching.pdf))
* Support failing over from one datacenter to another in under 1 minute (can you also think of a zero-downtime solution?) (CAP Theorem)
* Solve a concurrency issue.

**Artifacts (What you will turn in):**

* **Public Git Repo**
  + Initial Pitch Report
  + Initial Design
  + Progress log with entries that record time spent (in hours).
  + Demo video, gif, images, or markdown file.
  + Final Report
* **In Class and Class Channel**
  + Pitch
  + Feedback to others project ideas
  + Final Presentation *(presented in class \*and\* posted in class channel)*

* + - 3-10 minute presentation in class presentation (if you didn't present in class provide a recording in class channel).
    - Demonstrate your system, prototype, proof of concept, or a piece of your system in action. If you have no working code, be sure to show a design of your system.
    - Discuss why this project is interesting to you!
    - Summary of the project (one to three sentences)
    - Key learnings from the project (please try to come up with at least 3)
    - A diagram modeling the different parts of your system including the scaling characteristics of your system (find how your technologies scale by just testing it out or looking up the technology's documentation).
    - Explanation if applicable of failover strategy , performance characteristics, authentication, concurrency, etc.
    - Invite others to give feedback and/or ask questions!

**FAQ**

Q: I have no clue what to do or what this project is. What should I do?  
A: Talk to someone else in the class, the TAs, and myself. We are all here to help you succeed.

Q: I'd like to double count a project from another class, is that OK?  
A: If you are double counting a project from another class you need to put in the additional 20 to 40 hours into that project that you otherwise wouldn't have (double counting work projects is fine as long as you can share the results).

Q: I finished in less than 20 hours, is that OK?  
A: Yes, but start another project and spend 20-40 hours designing/building projects.

Q: Why are we doing this?  
A: You are a senior in computer science. I would like to give you an opportunity to use our class to **put your data modeling, SQL, and/or NoSQL skills to use**. I want you to have a great story and project to put on your **resume**that is really just yours. I want you to have some experience analyzing a system and what issues or bottlenecks it might have. I want you to have experience in technologies that will**enhance your future career** and opportunities. I want you to realize that you can learn to build something great without someone else telling you exactly what to do!

Q: How will this be graded?  
A: We are all counting on you to make the world a better place. The real test is how you will be better prepared or start now to do your life's work. So give it what you can! :) Your grade on this project will be determined by this quiz you fill out (submit as many times as you need to). Further you'll have checkpoints and opportunities to review other's projects.

Q: I'd really rather not do the in class presentation, could I do something else instead?  
A: Please talk yourself into doing the presentation. We love you! We'd love to hear from you and your ideas. If you can't succeed in talking yourself into it, don't don't be too discouraged! There are also extra credit items if you feel you need to make up the points with something else.

Q: What do reads and writes mean?  
A: This means it can't just be static data or data at rest. Something needs to be at least periodically updating it and something needs to read what has been written at some point. For example a static set of data that you can read real fast, but never changes isn't what we are looking for. Now if you think you have a great idea that is an exception to this, let me know!

Q: It is too open ended, I don't know what I'm doing or where to start. What should I do?  
A: Please sign up with the TAs or myself and we can help talk you through your ideas or suggest some.