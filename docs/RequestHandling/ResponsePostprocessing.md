# Response Postprocessing
There are often tasks when you need to add some elements for all states. For example, the "About skill" button.

The Response Post Processing input receives the context of the current call and the generated response. 
It returns the modified response

For create Post Processing, you need to create a class inherited from the `Trigger` class and redefine the abstract 
method `on_new_message`. You also need to register this post-processing in bot instance using 
```bot.add_post_processing_function(MyPostProcessing())``` 

This example add `About SKill` button to all responses
```python
# noinspection all
class MyPostProcessing(ResponsePostProcessing):
    def process(self, response: Response, skill_state: SkillState, user_state: State) -> Response:
        response.add_button(Button(title="About skill", payload={"my_button_id": "ABOUT_SKILL"}, hide=True))
        return response

bot.add_post_processing_function(MyPostProcessing())
```