<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/zach3697/RedboxInventoryManager">
    <img src="images/redboxTinkering.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Redbox Inventory Manager</h3>

  <p align="center">
    A tool meant to manage the inventory of a Redbox Machine (And add custom content!)
    <br />
    <!--<a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>-->
    <br />
    <br />
    <a href="https://youtu.be/uDMdTOeSMTo">View Intro Video</a>
    ·
    <a href="https://github.com/zach3697/RedboxInventoryManager/issues/new?labels=bug">Report Bug</a>
    ·
    <a href="https://github.com/zach3697/RedboxInventoryManager/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Product Name Screen Shot

This tool is meant to manage th inventory of a redbox kiosk including managing current titles, adding new title, assigning disk SN to inventory and (enventually) directly printing the barcodes from the application. 

Visit the Discord
https://discord.gg/r9MaZ9ZyWs


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

You can download the source code and start making your own customizations if desiered! Feel free to submit feature requests if there are things you feel should get incorporated. The project uses PyQt5 and Python to function. Here is some info about the structure of the application:

* The code was writen in Python 3.8-32 specifically so it could be run on the win7 OS that comes with most kiosk's (Some have been updagraded to windows 10)
* The Windows are designed with the Qt Designer application and can be used to edit the .ui files
* The app.config file contains variables that are loaded into the program at startup
* The DLL files in the assets folder contains the DLL files used for interacting with the various .data files

### Prerequisites (Development)

After downloading the files, make sure you have python 3.8-32bit installed and create a virtual environment as follows (Windows):
  ```sh
  python -m venv virt
  ```
Then activate the environment:
  ```sh
  virt/Scripts/activate.ps1
  ```
Once Activated, install the following dependencies:
  ```sh
  pip install PyQt5
  
  pip install pythonnet
  
  pip install slpp
  ```
  
  You can then run the main application: 
  ```sh
  python main2_1.py 
  ```

### Prerequisites (Production)

After downloading the files, you can run the main executable directly and start configuring the program:

### Installation

On the first run, you will need to specify the inventory.data and profile.data files, and the directory for the cover images to be accessed.

SCREENSHOT OF CONFIG PAGE


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Adding A Custom Title

You can add a custom title by clicking the add new button. This will populate all the fields with sample data. You do need to specify a unique product id which is a database key thats unique to each title (Beta limitation; Future release will not require this)

Fill out the remaining info as desiered for your title.

When selecting an image, you must manually place the selected image into the redbox cover directorty for the image to show up in the machine. (Beta Limitation; Future release will not require this)

Click Save and the custom title will be added to the database.

You should then add the serial number association to the inventry file

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Fix screen sizing to work on current redbox screen resolution of 1024x768
- [ ] Add ability for product id to be auto generated
- [ ] Incorporate print functionality for labels
- [ ] Add option to move the selected image to the correct directory on the kiosk automatically
- [ ] Add support for grouping products (ie having one title, but availibe in blu-ray, DVD, 4k etc)


See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Zach Kalb - zachkalb@gmail.com

Project Link: [https://github.com/zach3697/RedboxInventoryManager](https://github.com/zach3697/RedboxInventoryManager)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 

