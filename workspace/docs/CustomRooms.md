# Custom rooms

<!--
Things that should be fixed
* color tips (use gray shades)
-->

![Advanced custom room](./docs/ise.png)

## Introduction

Workspace Designer has an open file format so users can create their own custom rooms, independent of the strict template options in the wizard. This means you can add any objects you want anywhere you like in the room.

Some examples where this is needed:

* You have a completely different room type than what the Designer supports
* You have a different table or seating arrangement than the template supports
* You need to manually position microphones
* You have a non-standard displays setup
* You have a room with a non-rectangular shape
* You have an advanced room with multiple devices
* You have a room with an unusual camera configuration

The Designer supports a JSON-based proprietary file format that is easy to understand and manipulate. You can create custom rooms either manually or with other tools that support the same format. You can also start by creating a room with the standard Designer user interface, then export it and save the JSON file and edit it.


## Creating a custom room

There are three ways to create custom rooms.

### a) Write the JSON file yourself using a text editor (or start with one of our sample rooms)

When you have a room JSON file, you can simply drag and drop the file onto the 3d view of the Workspace Designer, and the file will be loaded.

### b) Use another tool that can export to the Workspace Designer JSON format.

One example of a third party tool that you can use is <a href="https://collabexperience.com" target="_blank">Video Room Calculator</a>. **Note**: This is not an officially supported tool from Cisco or Workspace Designer.

![VRC](./docs/vrc.png)

*Video Room Calculator with a flexible 2D drag and drop interface, exports directly to Workspace Designer*

### c) Export a template room to JSON, then modify it.

If you just need to make a few modifications to a room that you can create with the templates, you can hit **Ctrl-e** when you have a good basis (after exporting, you cannot edit the template options anymore). Save the JSON file and edit the objects that you want to change, and drag the file back in to the editor.

![Modified template](./docs/modified-template.png)

*Large template room exported, then manually added in a Table Mic Pro and an extra screen on the side wall*

## Example rooms

If you prefer to learn by example and trial and error rather than reading, you can quickly get started with these custom room examples:

<table class="examples">
  <tr>
    <td>
      <a href="#room/pod" target="_blank"><img src="./images/rooms/pod.png" /></a>
    </td>
    <td>
      <b>Pod</b>
      <p>
      Benches instead of seats, a third wall and a wall-mounted Navigator.
      <p>
    </td>
    <td>
      <a href="#room/pod" target="_blank">Preview</a>
      <p>
      <a href="./rooms/pod.json" download>Download</a>
    </td>
  </tr>
  <tr>
    <td>
      <a href="#room/huddle-skew" target="_blank"><img src="./images/rooms/huddle-skew.png" /></a>
    </td>
    <td>
      <b>Non-rectangular huddle room</b>
      <p>
      Room with skew window wall, a pouf and a couch.
      <p>
    </td>
    <td>
      <a href="#room/huddle-skew" target="_blank">Preview</a>
      <p>
      <a href="./rooms/huddle-skew.json" download>Download</a>
    </td>
  </tr>
  <tr>
    <td>
      <a href="#room/canteen" target="_blank"><img src="./images/rooms/canteen.png" /></a>
    </td>
    <td>
      <b>Townhall</b>
      <p>
      Mix of multiple table types, a custom small/large display setup, custom stage and ceiling-mounted presenter track camera and display.
      <p>
    </td>
    <td>
      <a href="#room/canteen" target="_blank">Preview</a>
      <p>
      <a href="./rooms/canteen.json" download>Download</a>
    </td>
  </tr>
  <tr>
    <td>
      <a href="#room/crossview-same-wall" target="_blank"><img src="./images/rooms/crossview-same-wall.png" /></a>
    </td>
    <td>
      <b>Cross-view on the same wall</b>
      <p>
      Two Vision PTZ in an alternative cross-view setup, and a 21:9 display.
      <p>
    </td>
    <td>
      <a href="#room/crossview-same-wall" target="_blank">Preview</a>
      <p>
      <a href="./rooms/crossview-same-wall.json" download>Download</a>
    </td>
  </tr>

  <tr>
    <td>
      <a href="#room/ise-2025" target="_blank"><img src="./images/rooms/ise2025.png" /></a>
    </td>
    <td>
      <b>ISE Cisco booth 2025</b>
      <p>
      Multiple rooms and devices, custom walls, screens everywhere, glass walls, coffee cups, pure madness - just like the real thing.
      <p>
    </td>
    <td>
      <a href="#room/ise-2025" target="_blank">Preview</a>
      <p>
      <a href="./rooms/ise-2025.json" download>Download</a>
    </td>
  </tr>
</table>

## What are the possibilities and limitations?

A lot of the core features of Workspace Designer also works well in custom rooms:

* Show your designs in full 3D from any angle of your choice
* Camera coverage and microphone coverage maps
* Green, yellow and red status for seats in the room
* In-camera views from any camera in your room
* Preview the on-screen experience and change screen content on all screens
* Blueprint with bill of materials for all items in the room
* Cable view if you use "standard floor/walls" and not more than one video device

The following limitations apply:

* You can no longer change video device, microphones, table options etc from the template system (settings in the side bar)
* You can only use the 3D objects provided by Workspace Designer, not your own
* Cable view will not be available in advanced scenarios

The complexity of complete freedom in design makes it hard to get everything right, and it is difficult for the Designer to
give perfect recommendations in all possible scenarios, so please keep this in mind. But if you do find issues, please join the [Workspace Designer
feedback space](https://eurl.io/#ejV0ptTs8) in Webex and describe your issue there, it's an active community where you are likely to get a response quickly.


## The room JSON file


This is an example of a full JSON file containing a chair, a screen, a video bar.

```json
{
  "title": "Example room",
  "roomShape": {
    "manual": true,
    "width": 4,
    "length": 5,
    "height": 2.5
  },
  "customObjects": [
    {
      "id": "chair1",
      "objectType": "chair",
      "position": [0, 0, 0],
      "rotation": [0, -1.57, 0]
    },
    {
      "id": "roombar",
      "objectType": "videoDevice",
      "model": "Room Bar",
      "color": "light",
      "position": [-1.9, 1.75, 0],
      "rotation": [0, 1.57, 0]
    },
    {
      "id": "screen1",
      "objectType": "screen",
      "position": [-1.9, 1.2, 0],
      "scale": [1, 1, 1],
      "rotation": [0, 1.57, 0],
      "size": 75,
      "role": "singleScreen"
    },
    {
      "id": "plant1",
      "objectType": "plant",
      "position": [1.5, 0, -1.5]
    }
  ]
}
```

![Example room](./docs/example.png)



The floor and wall in this case is generated by the Designer by the template setting `roomShape`. If desired, you can skip that and create the floor and walls yourself, for example if you need a room with a non-rectangular shape.

## Coordinate system

The coordinate system is defined by a 3D array (vector) where `x` is the direction of the width of the room, `y` is the height direction, and `z` is in the direction of the length of the room. The origin `[0, 0, 0]` is in center of the room on the floor.

![Coordinate system](./docs/coordinate-system.png)

Assuming a standard template room with a device/screen on the video wall.

### Position

When you set the position of an object, you set where it's mount point is. The mount point may be different places on the object, depending on it's type, but usually how you would mount it in the "real world". Eg a chair has it's mount point on the bottom center, whereas a Room Bar has it's mount point on the vertical center on the back of the bar.

| Property | Description |
| --- | --- |
| Origin | The center of the room, on top of the floor |
| x | Positive towards the right when looking at the wall that usually has a screen |
| y | Positive upwards |
| z | Positive away from the wall that usually has a screen |
| unit | Distance is always in meters |

### Rotation

![Rotations](./docs/rotations.png)

Orientation can happen on all 3 axis. The order of rotation is `y` (spin), `x` (tilt), then `z` (lean). This is the natural yaw-pitch-roll order you typically would expect. Most objects only need to be rotated in the `y` direction, ie which wall it is facing in the room.

The default orientation of an object is to face out into the room along the `z-axis`, basically like the main display in the room.

| Property | Description |
| --- | --- |
| y | The 'heading' of the object. 0 typically means facing the same direction as the main camera. Positive direction anti-clockwise |
| x | The 'tilt' of the object. Positive direction tilting downwards. |
| z | The 'slant' of the object. Positive direction slanting left |
| unit | radians. 0 is 0 degrees, 1.57 is 90 degrees, 3.14 is 180 degrees, etc|


### Scale

The property `scale` is a vector3, and defaults to `[1, 1, 1]`. You usually don't need to change this, as most objects have more dedicated parameters to adjust their size. Setting the scale to `[2, 1.5, 3]` will make the object twice as wide, 50% higher and 3 times longer.

**Tip**: Negative scales are allowed, this will mirror the object.

## Objects

Objects can be added to the scene, by using the `customObjects` list. The following properties are available to most object types:

| Parameter   | Value  |
| ---         | --- |
| id          | Object id, can be any string you choose, the value doesn't matter, but each id must be unique. |
| objectType  | Type of object, such as videoDevice, floor, wall, chair etc. See each type below. |
| model       | Sub type, eg which kind of video device, microphone, table etc you want.
| position    | 3 element vector, eg [1, 1.8, 4] will be placed in x=1, y=1.8 (height) and z=4. Optional and defaults to [0, 0, 0]. |
| rotation    | 3 element vector in radians, eg [0, 3.14, 0] will rotate the object's orientation to face the opposite direction of default. Optional and defaults to [0, 0, 0] |
| scale       | 3 element vector scaling the object in each axis, default [1, 1, 1] |


In addition, each object type might have more specific properties, see below.




<!-- TODO: Just make a table with all object types, models, available parameters instead -->


### Wall, floor, ceiling

**Note:** If you specify the `roomShape` setting as described in the JSON example above, you don't need to specify walls, floors or ceilings yourself, if you are happy with the default ones that the Designer provides.

| Parameter   | Value |
| ---         | ---  |
| objectType  | wall |
| model | basic (default), glass, window |
| width       | The long side of the wall (m) |
| length      | The thickness of the wall. Default: 0.1m |
| height      | The height of the wall (m) |
| rotation | vector 3 (radians) |
| color       | color (#333333, orange, etc) |

Walls gets resized according to the size you give them. The position given is the center of the box. You can set the properties `width`, `length` and `height` to size them. Set the second (y) value of`rotation` to rotate the wall to the direction you want. The position is the the center of the wall, so you may need to do some math to position them exactly to line up with other walls.

**Note that `length` is the thickness of the wall. This API might change slightly at a later date.**

When `objectType` is `floor` or `ceiling`, just use the `scale` property to set the dimensions.

![Example with floor and wall](./docs/wall.png)

*Image and JSON example of a floor and a window wall*

```json
{
  "customObjects": [
    {
      "id": "floor",
      "objectType": "floor",
      "position": [0, -0.05, 0],
      "scale": [3, 0.1, 4]
    },
    {
      "id": "windowwall",
      "objectType": "wall",
      "model": "window",
      "width": 3,
      "length": 0.1,
      "height": 2.8,
      "position": [0, 1.4, 0],
      "rotation": [0, 1.0, 0]
    }
  ]
}
```


### Video device

You can add any of the supported Cisco video devices as objects in the room, and set position, orientation etc. Some devices support different mounts, colors and screen sizes. For kits, the position is for the quad camera, not the codec.

| Parameter   | Value       |
| ---         | ---         |
| objectType  | videoDevice |
| model       | Room Bar, Room Bar Pro, Room Kit Pro, Room Kit EQ, EQX, Board Pro |

Additional parameters:

| model        | mount                              | color       | size   |
| ------------ | -----------------------            |------------ | ------ |
| Room Bar     | wall                               | dark, light |        |
| Room Bar Pro | wall                               | dark, light |        |
| Room Kit Pro | wall                               | dark, light |        |
| Room Kit Pro G2 | wall | dark, light | | |
| Room Kit EQ  | wall                               | dark, light |        |
| EQX          | wall, wallstand, floor             |             |        |
| Board Pro    | wall, floor, wallstand, wheelstand |             | 55, 75 |
| Desk Pro G2  | desk, wall | |
| Desk Pro     | desk, wall                                   |             |        |
| Desk         |                                    |             |        |
| Desk Mini    |                                    |             |        |

Eg to add a Room Kit EQX:

```json
{
  "id": "myeqx",
  "objectType": "videoDevice",
  "model": "EQX",
  "mount": "wallstand",
  "position": [0, 1.8, 2],
  "rotation": [0, 3.14, 0]
}
```

Add a light Room Bar:

```json
{
  "id": "myroombar",
  "objectType": "videoDevice",
  "model": "Room Bar",
  "color": "light",
  "position": [0, 1.8, 2]
}
```

Note that the appropriate mount height (y position) of a device dependents on the mount type. For bars, it's simply the y position where you want to mount the bar (eg 1.0 if below displays, or when above displays calculated based on the display height for the chosen display size). When using floor mount or floor stand, y should be 0 (so the device is firmly on the floor).

The Designer will automatically provide ranges, field of views, in-camera views etc for the given device type.


### Microphones

| Parameter   | Value       |
| ---         | ---         |
| objectType | microphone |
| model |  Table Mic Pro, Table Mic, Ceiling Mic Pro, Ceiling Mic |

Mounts are currently not supported for custom models.

```json
{
  "id": "mic1",
  "objectType": "microphone",
  "model": "Table Mic Pro",
  "position": [0, 0.7, 0],
}
```

The Designer will automatically create ranges and coverage plots for the microphones added.

### Cameras

| Property | Values |
| ---- | ---- |
| objectModel | camera |
| model | ptz, quad, vision |
| color | light, dark <sup>1</sup>|
| role | crossview, extended_reach, presentertrack|

<sup>1</sup> Not for PTZ camera

A PTZ presenter track camera can be added like this:

```json
{
  "id": "my-presenter-cam",
  "objectType": "camera",
  "model": "ptz",
  "role": "presentertrack",
  "position": [0, 2, 0],
  "rotation": [0, 1.57, 0]
}
```

The Designer will automatically create ranges, field of view and coverage plots for the cameras added, based on the camera type and the role.

To mount a camera upside down, set `"scale": [1, -1, 1]`. This is better than changing orientation, as this may have other side effects.

### Screens

| Parameter   | Value       |
| ---         | ---         |
| objectType | screen |
| model | lcd (default), canvas |
| aspect | 16:9 (default), 21:9 |
| position | vector 3, the center of the screen |
| size | The screen diagonal size in inches |
| role | singleScreen, firstScreen, secondScreen, thirdScreen (for presenter track scenarios), navigator, scheduler laptop |

They `y` position is the center of the screen, so you will need to calculate it based on your desired setup as well.

There is a small additional bezel to the screen that also gets scaled up proportional with the screen size (but the depth remains unchanged) - you may need to account for this when placing screens next to each other.

To determine what content goes on the screen, use the `role` property.

| Role | Description |
| --- | --- |
| singleScreen | Shows both share content and PiP of far end participants on the same screen |
| firstScreen | In call: presentation if available, otherwise grid of people |
| secondScreen | In call: far end presenter on first screen, presentation on second screen |
| navigator | The navigator UI |
| scheduler | The scheduler UI (changes depending on whether there are people in the room) |
| laptop | The share screen content |

If you supply a screen with `thirdScreen` role, things change a bit. Workspace Designer then assumes that you have classroom/briefing room mode, and puts far end participants on the third screen, far end presenter on first screen and presentation on second screen. Not available in MTR mode.

**Note**: You can use `canvas` as `model`. The only difference is a slight change in appearance, and it will be specified as a projector canvas in the blueprint. In that case, you may want to use an object of type `projector` too. The Projector will receive the cable that the screen normally would have gotten.

### Custom screen content

You can put your own images on any screen in the Workspace Designer. This is useful for branding and can make your design stand out and feel more relevant to the customer. The custom image will override the image that is normally placed on the screen, and remains even if the user changes device state (home screen, in-call etc). The images will also be shown in the blueprint.

**Note**: There is no way to upload your image to Workspace Designer, so you will need to either use an image that is already publicly available on the Internet, or host it yourself. [GitHub Pages](https://pages.github.com) is a quick and simple, free alternative, or you can find many royalty-free images on services like [Unsplash](https://unsplash.com).

Use the `contentUrl` to set the content. Example:

```
{
  "id": "myscreen",
  "objectType": "screen",
  "size": 85,
  "position": [0, -2, 0],
  "contentUrl": "https://images.unsplash.com/photo-1755371034010-51c25321312d"
}
```

It's recommended to use an image with a resolution of 1080 pixels high, and match the aspect of the screen (16:9 or 21:9).

Here are a few ideas of what to put on screen:

* Your own branding / logo if you are a partner
* Branding of the customer you are designing a room for
* A product illustration / PowerPoint slide for the customer
* An in-call illustration with actual customer faces
* Specific video user experiences you want to highlight (classroom modes, People Focus,e tc)

Obviously, Workspace Designer takes no responsibility or ownership for the content you choose to put there.

### Phones

Currently the Cisco 9800-series is supported.

| objectType  | model                     | color       |
| ------------| ------------------------- | ----------- |
| phone       | 9871, 9861, 9851, 9851    | dark, light |

Set the `role: phone` to get content on screen.


### Navigators

| Parameter   | Value       |
| ---         | ---         |
| objectType | navigator, scheduler |
| role | navigator, scheduler |

Be sure to also st the `role` to get screen content on them.

### Peripherals and accessories


| objectType  | model                             |
| ----------- | --------------------------------- |
| headset     | 980, 950, 730, 720, 560, 530, 320 |
| webcam      | 4k, 1080p                         |



### Tables


| Parameter   | Value       |
| ---         | ---         |
| objectType | table |
| position | vector 3, usually the center of the table |
| model | regular, tapered, ushape, round, schooldesk, podium |
| width | The width of the table (for tapered table, this is the width at the narrow end) |
| length | The length of the table (in meters) |
| taper | The additional width (in meters) at the wide end (tapered tables only) |
| radius | For corner radius (in meters, not used for u-shaped tables). |
| radiusRight | The radius of the far side of the table, in meters. If not specified, it's the same as radius. The reason for this one is to create a table that is round on one edge and not on the other, typically when set against the wall. |

For a round table, use `length` to set the diameter of the table. All tables are 0.71 m high, except for the podium which is 1 m.

### Chairs

| Parameter   | Value       |
| ---         | ---         |
| objectType | chair |

The chair is the object that the Designer uses in the coverage analysis to check whether people are within the ranges of the camera, the microphones and the displays.

The Designer will automatically populate people on the chairs, so don't put persons on the chair yourself.

## Ignored chairs

Sometimes you need chairs in the room for people that are not meant to be part of the conversations, eg note takers or technical staff. In this case, you can add `ignore: true` to the object. This will prevent the chair from being part of the various analysis (camera, microphone, display coverage etc). It will also disappear when you view the coverage views, to indicate that they are not considered.

### People

People are automatically added to the chairs. If you need to place people yourself, you can define them like this:

| Parameter   | Value       |
| ---         | ---         |
| objectType | person |
| model | woman-standing, man-standing-pen, man-sitting-bald, man-sitting-curly, man-sitting-leaning, man-sitting-old, man-sitting-young, woman-sitting-curly, woman-sitting-engaged, woman-sitting-ponytail, woman-sitting-wheelchair |

```json
{
  "id": "person1",
  "objectType": "person",
  "model": "woman-standing",
  "position": [1, 0, 1],
  "rotation": [0, 1.8, 0]
}
```

You can tweak the scale values (`y` for height and `x` for width) to vary the same model. Set scale `x` to `-1` to mirror the person.

**Note**: Currently, people defined by you will not be part of the coverage analysis.

### Laptop

| Parameter   | Value       |
| ---         | ---         |
| objectType | laptop |
| role | laptop |

Remember to also set the `role` to get content on the screen.

### Box

You can use a box as a generic object such as a column or a simple credenza, etc.

| Parameter   | Value       |
| ---         | ---         |
| objectType | box |
| width | number |
| length | number |
| height | number |
| color | #ff988cc, pink |

It's recommended to use `width`, `length` and `height`, but if you use `scale` instead, that will take precedence.


### Basic shapes

These basic shapes can typically be used as Lego blocks to create objects you need in the room that is not already supported by
the built-in objects.

| objectType | Properties |
| ---         | --- |
| sphere | radius, position, color |
| cylinder | length, radius, position, rotation, color |


### Text objects

Text objects are physical letters than you can put on walls etc as sign posts.

| Property | Valuespace | Description |
| --- | --- | --- |
| objectType | text | |
| position | V3 | The bottom left coordinate of the first line |
| text | string | The actual text content |
| color | text | The color of the text |
| size | number | Font size. A value of 10 gives ca 10 cm high letters.

You can use "\n" to force new lines.

Example:

```json
{
  "id": "roomname",
  "objectType": "text",
  "text": "Executive suite",
  "position": [0, 1, 0],
  "size": 20,
  "color": "black"
}
```

### Other objects

| Parameter   | Value       |
| ---         | ---         |
| objectType | door, plant, door, wheelchair, pouf, couch, credenza, projector, loudspeaker |

There may be many additional object types added to the Designer later, based on how popular the custom rooms will be.

<!--
## Combining custom objects and the template system

If you mostly want a standard room, but still want to do some tweaks, it's also possible to pick and choose some of the template options. For example, here is a standard large room with additional "spectator" chairs added at the sides of the room. Instead of specifying the table, the video device, the microphones etc manually, the template options are specified as settings in the JSON file, and only the extra chairs are added as custom objects. This means the sidebar options are still available, so you can easily change the video device type etc.

[JSON example](./rooms/custom-largeroom.json)

![Custom room with template options](./docs/custom-template.png)

To see the syntax of the template options, see the JSON for these rooms as examples:

[Huddle](./rooms/huddle.json) [Small](./rooms/small.json)
 -->

## FAQ

### How do I flip a camera upside down?

Set `"scale": [1, -1, 1]`. This is better than changing the rotation, which will cause issues with coverage plots.

### Can I remove the audio treatment on the default walls, they are crashing with some of my own objects?

Not currently.

### Why isn't cable view showing up?

Cable view is not supported if you have more than one video device.

### Can I set my own camera presets / viewpoints?

Not currently.

### Why can't I just drag and drop objects in the Designer itself?

The Workspace Designer dev team contains less than a handful developers, and a full drag and drop interface (although highly desirable) is currently beyond the scope of this team. We will re-evaluate this if the custom rooms prove to be a very popular feature.

### Why does the 3D view flicker?

This is a common problem in 3D called <a href="https://en.wikipedia.org/wiki/Z-fighting" target="_blank">z-fighting</a>. This occurs when multiple objects overlap the same exact space. To avoid this, try repositioning or rescaling one of the overlapping objects slightly.

### Why don't I see screen content on one of my objects?

Remember to set the `role` property for the object too.

### What's wrong with my JSON?

The custom rooms format is JSON. If you edit manually, be sure to avoid the following common mistakes, that are supported by normal JavaScript but not JSON:

```json
{
  // comment
  url: "https://acme.com",
  "width:": 3,
  "size": 12,
}
```

1. Comments are not supported in JSON. If you still want to comment, create a dummy element, eg `"comment": "mycomment"`

2. Unlike JavaScript, keys like `url` above need to be enclosed in " (quotation marks). Only use the double marks ", not the single '.

3. Avoid dangling commas, like after the number 12 above.

4. The width property above accidentally has a colon inside the name. This can be hard to spot when debugging.

Fixed:

```json
{
  "comment": "my comment",
  "url": "https://acme.com",
  "width": 3,
  "size": 12
}
```

## Useful tips

- Turn on measurement mode to see grid.
- Open the browser's developer console to see if there are any errors


## Advanced: Custom shapes

![Custom shapes](./docs/custom-table.png)

It is possible to create custom shapes by defining a shape and then controlling the thickness of it, similar to how you would form a flat gingerbread cake and then grow it in the oven. This can be useful to create custom table shapes or other objects that are not represented by the standard objects mentioned in this guide.

To use custom shapes, you need a basic understanding of SVG path shapes. This is a 2-dimensional shape format that supports lines, curves, circles and ellipsis.

The `x` and `y` coordinates of the path is mapped to the `x` and `z` coordinates in Workspace Designer, so that path will be a flat shape parallell to the ground - like a table surface.

For example, to define a video centric table:

```json
{
  "id": "my-vdeo-table",
  "objectType": "shape",
  "path": "M -1.4 0 Q 0 1.4 1.4 0 L 1 -0.4 Q 0 0.6 -1 -0.4 Z",
  "position": [0, 0.7, 0],
  "thickness": 0.05
}
```

Keep in mind:

* Center your object around 0,0 - so it's easy to move the object around in your room in a predicable and consistent manner similar to the standard objects.
* Use meter as unit for your path. Even if you use feet in the user interface, the unit in the JSON model for custom rooms is always metric.
* You can't create objects with holes in them.
* You can of course rotate the custom shapes around all axes like any other objects.
* You can only have one path segment per object - if you need more, just create multiple objects.

If you need a hollow object, such as a donut table, make the halves and put them together.

There is no support for the table legs currently, but this will come soon. In the meantime you can use eg simple boxes as a base for the table to stand on.

### How do I learn how to make SVG paths?

The simplest is perhaps just to use an interactive online SVG tool, such as [this SVG editor](https://yqnn.github.io/svg-path-editor/). Tools like this let you visually see your changes live, drag and drop points, move and scale the object easily and basically just play with it, even if you have never used SVG paths before.

