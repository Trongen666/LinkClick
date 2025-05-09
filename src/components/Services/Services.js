import React from 'react';
import './Services.css';

const services = [
  {
    name: 'Netflix Website',
    imgSrc: 'https://1000logos.net/wp-content/uploads/2017/05/Netflix-Logo-500x281.png',
    howToUseLink: 'https://help.netflix.com/en/',
  },
  {
    name: 'Amazon Shopping',
    imgSrc: 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg',
    howToUseLink: 'https://www.amazon.in/gp/help/customer/display.html',
  },
  {
    name: 'Amazon Prime Video',
    imgSrc: 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Prime_Video.png',
    howToUseLink: 'https://www.primevideo.com/help',
  },
  {
    name: 'Disney Hotstar',
    imgSrc: 'https://play-lh.googleusercontent.com/bp4jknyVZ8yDKhER9thIS1p9MBeU2LABqBX-sO8uaL1h5_keqlgMUmXv-CjfRWaqKw',
    howToUseLink: 'https://www.hotstar.com/in/help',
  },
  {
    name: 'Pension & Finance',
    imgSrc: 'https://images.deepai.org/art-image/796cb4dbb1d4411087e6c49bea5924ad/a-wallet-with-rupee-coins-and-a-pension-slip-with-an-.jpg',
    howToUseLink: 'https://www.myscheme.gov.in/schemes/nsap-ignoaps',
  },
  {
    name: 'ID & Documentation',
    imgSrc: 'https://images.deepai.org/art-image/dc9e272be0914eee9a077f24bd75cdc6/an-aadhaar-card-and-a-mobile-phone-showing-life-certi.jpg',
    howToUseLink: 'https://uidai.gov.in/en/',
  },
  {
    name: 'Legal & Emergency',
    imgSrc: 'https://images.deepai.org/art-image/b2910b0da8ea4b1a8e555145e157b186/a-shield-icon-with-a-phone-number-14567-and-a-senior-.jpg',
    howToUseLink: 'https://www.ready.gov/older-adults',
  },
];

const Services = () => {
  return (
    <div className="services-container">
      <h2>Explore Our Services</h2>
      <div className="services-grid">
        {services.map((service, index) => (
          <a
            key={index}
            href={service.howToUseLink}
            target="_blank"
            rel="noopener noreferrer"
            className="service-card"
          >
            <img src={service.imgSrc} alt={service.name} />
            <span className="service-link">{service.name}</span>
          </a>
        ))}
      </div>
    </div>
  );
};

export default Services;
