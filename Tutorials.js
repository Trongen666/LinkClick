import { useState } from 'react';

// Tutorial data from your JSON file
const tutorialData = [
  {
    "tutorialCategory": "Transport",
    "tutorials": [
      {
        "description": "Cab booking (Hindi)",
        "videoLink": "https://www.youtube.com/watch?v=Ho8qiFmNOlU",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/uP_6Pts2GL4/hq720.jpg"
      },
      {
        "description": "Cab booking (Telugu)",
        "videoLink": "https://www.youtube.com/watch?v=MlHUiIggEYA",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/l2OsPGlDyfA/hqdefault.jpg"
      },
      {
        "description": "Cab booking (English)",
        "videoLink": "https://www.youtube.com/watch?v=pP8QezUqSO0",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/xyQgptuIcpw/maxresdefault.jpg"
      }
    ]
  },
  {
    "tutorialCategory": "Food",
    "tutorials": [
      {
        "description": "Swiggy (Hindi)",
        "videoLink": "https://youtu.be/mJyOjygO9eU",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/KGCC1XXDwws/maxresdefault.jpg"
      },
      {
        "description": "Swiggy (Telugu)",
        "videoLink": "https://youtu.be/JBp2H--OlBg",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/3U7yIlRoYds/hq720.jpg"
      },
      {
        "description": "Swiggy (English)",
        "videoLink": "https://youtu.be/dY6_IjA-O9w",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/orOdajUOC6o/hqdefault.jpg"
      },
      {
        "description": "Zomato Ordering (Hindi)",
        "videoLink": "https://youtu.be/M6c05tz9nu0",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/6ZLcrWGu6Vw/maxresdefault.jpg"
      },
      {
        "description": "Zomato Ordering (Telugu)",
        "videoLink": "https://youtu.be/TaQHVbEyqWQ",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/E4Yff1YZrso/maxresdefault.jpg"
      },
      {
        "description": "Zomato Ordering (English)",
        "videoLink": "https://youtu.be/Cvpz0qY1Mas",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "/api/placeholder/320/180"
      }
    ]
  },
  {
    "tutorialCategory": "House Repairs",
    "tutorials": [
      {
        "description": "Urban Company (Hindi)",
        "videoLink": "https://www.youtube.com/watch?v=V-PKgDXgU7Q",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/3mphDEOonus/maxresdefault.jpg"
      },
      {
        "description": "Urban Company (Telugu)",
        "videoLink": "https://www.youtube.com/watch?v=VFsMHVf4L8c",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "/api/placeholder/320/180"
      },
      {
        "description": "Urban Company (English)",
        "videoLink": "https://www.youtube.com/watch?v=OK-aBOgTbMA",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/VFsMHVf4L8c/sddefault.jpg"
      }
    ]
  },
  {
    "tutorialCategory": "Online Shopping",
    "tutorials": [
      {
        "description": "Amazon (Hindi)",
        "videoLink": "https://youtu.be/2pGji01WY1U",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/Hm9Jq03FegQ/hq720.jpg"
      },
      {
        "description": "Amazon (Telugu)",
        "videoLink": "https://youtu.be/DZmeWpxaBTI",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/qw3-FX1fCqU/maxresdefault.jpg"
      },
      {
        "description": "Amazon (English)",
        "videoLink": "https://youtu.be/rDylGAcqF7U",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/x0cESERAp2M/hq720.jpg"
      },
      {
        "description": "Big Basket (Hindi)",
        "videoLink": "https://youtu.be/0ooPhA5_AvM",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/0ooPhA5_AvM/hq720.jpg"
      },
      {
        "description": "Big Basket (Telugu)",
        "videoLink": "https://youtu.be/s-fQT6-kL2E",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/s-fQT6-kL2E/sddefault.jpg"
      },
      {
        "description": "Big Basket (English)",
        "videoLink": "https://youtu.be/L6Umq9zVZ24",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/dKzs2mTTouU/hq720.jpg"
      }
    ]
  },
  {
    "tutorialCategory": "Finance",
    "tutorials": [
      {
        "description": "UPI PhonePe (Hindi)",
        "videoLink": "https://youtu.be/2ky-tWGD13Q",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/2ky-tWGD13Q/maxresdefault.jpg"
      },
      {
        "description": "UPI PhonePe (Telugu)",
        "videoLink": "https://youtu.be/RwKZTvBH7JM",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/4NP0UPvH4Ys/maxresdefault.jpg"
      },
      {
        "description": "UPI PhonePe (English)",
        "videoLink": "https://youtu.be/EsmAFKKfwDQ",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/EsmAFKKfwDQ/hq720.jpg"
      },
      {
        "description": "UPI Google Pay (Hindi)",
        "videoLink": "https://youtu.be/UwXzg3YShzA",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/UwXzg3YShzA/maxresdefault.jpg"
      },
      {
        "description": "UPI Google Pay (Telugu)",
        "videoLink": "https://youtu.be/ZI2SCuhN2Mw",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/ZI2SCuhN2Mw/maxresdefault.jpg"
      },
      {
        "description": "UPI Google Pay (English)",
        "videoLink": "https://youtu.be/NoYzau-zfJg",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/-E8IQ8jekkQ/maxresdefault.jpg"
      }
    ]
  },
  {
    "tutorialCategory": "OTT",
    "tutorials": [
      {
        "description": "Netflix (Hindi)",
        "videoLink": "https://www.youtube.com/watch?v=OK-aBOgTbMA",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06", 
        "thumbnail": "https://i.ytimg.com/vi/CTYW-hAm4vQ/maxresdefault.jpg"
      },
      {
        "description": "Netflix (Telugu)",
        "videoLink": "https://www.youtube.com/watch?v=VFsMHVf4L8c",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/50O_-Ep_iSc/hq720.jpg"
      },
      {
        "description": "Netflix (English)",
        "videoLink": "https://www.youtube.com/watch?v=V-PKgDXgU7Q",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/BvU7WT2B5hE/maxresdefault.jpg"
      },
 {
        "description": "Jio Hotstar (Hindi)",
        "videoLink": "https://youtu.be/ZFHzqJyJKSg",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06", 
        "thumbnail": "https://i.ytimg.com/vi/ZFHzqJyJKSg/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCPZm7IMf6twJRaonO0-IDvyPPkRA"
      },
      {
        "description": "Jio Hotstar (Telugu)",
        "videoLink": "https://youtu.be/4bvFXvW11UM",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/4bvFXvW11UM/maxresdefault.jpg"
      },
      {
        "description": "Jio Hotstar (English)",
        "videoLink": "https://youtu.be/ozgUnZ67wXQ",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/ozgUnZ67wXQ/maxresdefault.jpg"
      },
      {
        "description": "Prime (Hindi)",
        "videoLink": "https://youtu.be/-v2X4nXYNcs",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/hASFzgX9gmE/hq720.jpg"
      },
      {
        "description": "Prime (Telugu)",
        "videoLink": "https://youtu.be/F35Er9e2Ago",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/Sm7X7F9-WFQ/hq720.jpg"
      },
      {
        "description": "Prime (English)",
        "videoLink": "https://youtu.be/NjVRAO7lxBA",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/7G7RyXzHMSM/maxresdefault.jpg"
      }
    ]
  },
  {
    "tutorialCategory": "Social Media",
    "tutorials": [
      {
        "description": "Facebook (Hindi)",
        "videoLink": "https://www.youtube.com/watch?v=Yp3JVqR2jew",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/IjWquvjG_o0/maxresdefault.jpg"
      },
      {
        "description": "Facebook (Telugu)",
        "videoLink": "https://www.youtube.com/watch?v=DP2pCxDWf_s",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/GP5MBYx3RRY/sddefault.jpg"
      },
      {
        "description": "Facebook (English)",
        "videoLink": "https://www.youtube.com/watch?v=xu8rh9Ref4Y",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/xu8rh9Ref4Y/maxresdefault.jpg"
      },
      {
        "description": "WhatsApp (Hindi)",
        "videoLink": "https://www.youtube.com/watch?v=d3VWmsb0ZXA",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/B086mysgDs4/hq720.jpg"
      },
      {
        "description": "WhatsApp (Telugu)",
        "videoLink": "https://www.youtube.com/watch?v=T6exB49AgD8",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/T6exB49AgD8/maxresdefault.jpg"
      },
      {
        "description": "WhatsApp (English)",
        "videoLink": "https://www.youtube.com/watch?v=sghayXZ_RK0",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "/api/placeholder/320/180"
      },
      {
        "description": "Instagram (Hindi)",
        "videoLink": "https://www.youtube.com/watch?v=ksFH1Ka8Nuo",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/ksFH1Ka8Nuo/maxresdefault.jpg"
      },
      {
        "description": "Instagram (Telugu)",
        "videoLink": "https://www.youtube.com/watch?v=W5Q7p-nMIR4",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "https://i.ytimg.com/vi/0i3W0oE22ec/maxresdefault.jpg"
      },
      {
        "description": "Instagram (English)",
        "videoLink": "https://www.youtube.com/watch?v=2YSB468mn4M",
        "uploadedBy": "userLC",
        "uploadedDate": "2025-05-06",
        "thumbnail": "/api/placeholder/320/180"
      }
    ]
  },
{
    "tutorialCategory": "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
    "tutorials": [
        { 
          "description": "(english)Ayushman Bharat PM-JAY is the world's largest health assurance scheme, offering health coverage of ₹5 lakhs per family per year for secondary and tertiary care hospitalization to over 12 crore poor and vulnerable families. As of September 2024, the scheme has been expanded to include all senior citizens aged 70 and above, irrespective of income.",
          "videoLink": "https://www.youtube.com/live/oJW9ccz1qik?si=WyX84Z5H7PpJSuIo",
          "uploadedBy": "EduTap",
          "uploadedDate": "2023-08-15",
          "thumbnail": "https://i.ytimg.com/vi/oJW9ccz1qik/maxresdefault.jpg"
        },
        {
            "description": "(hindi)Ayushman Bharat PM-JAY ",
            "videoLink" : "https://youtu.be/SToefGBjhbM?si=V3COyR9GmFVba83Q",
            "uploadedBy": "Swasth Bharat",
             "uploadedDate": "2023-09-10",
             "thumbnail": "https://i.ytimg.com/vi/SToefGBjhbM/maxresdefault.jpg"
        },
        {
            "description": "(telugu)Ayushman Bharat PM-JAY ",
          "videoLink": "https://youtu.be/rmLfdeUCXfM?si=rCvYaIpFZ--yMA8r",
          "uploadedBy": "Mana Arogya",
          "uploadedDate": "2023-10-01",
          "thumbnail": "https://i.ytimg.com/vi/rmLfdeUCXfM/maxresdefault.jpg"
        }
    ],
 },
 {
    "tutorialCategory": "Atal Pension Yojana (APY)",
    "tutorials": [
        { 
          "description": "(english) APY",
          "videoLink": "https://youtu.be/rPX6LnlCwsA?si=DIz7o52fVbp2xuhZ",
          "uploadedBy": "Financial Literacy India",
          "uploadedDate": "2023-07-20",
          "thumbnail": "https://i.ytimg.com/vi/rPX6LnlCwsA/maxresdefault.jpg"
        },
        {
            "description": "(hindi)APY ",
            "videoLink": "https://youtu.be/h_3NMIwq4rE?si=DvLZhgZWzB-4T2hw",
          "uploadedBy": "Nivesh Ki Pathshala",
          "uploadedDate": "2023-08-05",
          "thumbnail": "https://i.ytimg.com/vi/h_3NMIwq4rE/maxresdefault.jpg"
        },
        {
            "description": "(telugu)APY",
          "videoLink": "https://youtu.be/GreqdBrHgpY?si=tR54eZsVaVSJhaoL",
          "uploadedBy": "Telugu Money Guide",
          "uploadedDate": "2023-08-25",
          "thumbnail": "https://i.ytimg.com/vi/GreqdBrHgpY/maxresdefault.jpg"
        }
    ],
 },
 {
    "tutorialCategory": "Senior Citizens' Savings Scheme (SCSS)",
    "tutorials": [
        { 
          "description": "(english) SCSS",
          "videoLink": "https://youtu.be/7mrUsThbC2o?si=ga0dQJ0rDcR3-sED",
          "uploadedBy": "Investment Insights",
          "uploadedDate": "2023-06-15",
          "thumbnail": "https://i.ytimg.com/vi/7mrUsThbC2o/maxresdefault.jpg"
        },
        {
            "description": "(hindi)SCSS ",
            "videoLink": "https://youtu.be/EqmSsB15UlQ?si=UDewr3ONEEOJslkg",
          "uploadedBy": "Arthik Gyaan",
          "uploadedDate": "2023-07-10",
          "thumbnail": "https://i.ytimg.com/vi/EqmSsB15UlQ/maxresdefault.jpg"
        },
        {
            "description": "(telugu)SCSS",
            "videoLink": "https://youtu.be/dID2jRXiT6I?si=-aevOppMA3ygX10b",
            "uploadedBy": "Telugu Finance World",
            "uploadedDate": "2023-07-25",
            "thumbnail": "https://i.ytimg.com/vi/dID2jRXiT6I/maxresdefault.jpg"
        }
    ],
 },
 {
    "tutorialCategory": "Atal Vayo Abhyuday Yojana (AVYAY)",
    "tutorials": [
        { 
          "description": "(english) AVYAY",
          "videoLink": "https://youtu.be/W4pvZfRZ1Qw?si=XBeIIqWew3hSTCRs",
          "uploadedBy": "Social Welfare India",
          "uploadedDate": "2023-05-20",
          "thumbnail": "https://i.ytimg.com/vi/W4pvZfRZ1Qw/maxresdefault.jpg"
        },
        {
            "description": "(hindi)AVYAY ",
            "videoLink": "https://youtu.be/hlC9rD5kiXY?si=nRNoa6GrqmZFRnjs",
          "uploadedBy": "Samajik Kalyan",
          "uploadedDate": "2023-06-05",
          "thumbnail": "https://i.ytimg.com/vi/hlC9rD5kiXY/maxresdefault.jpg"
        },
        {
            "description": "(telugu)AVYAY",
            "videoLink": "https://youtu.be/0LXopQsi8Cc?si=bU8xAc8PnQmIXtvB",
          "uploadedBy": "Mana Seva",
          "uploadedDate": "2023-06-20",
          "thumbnail": "https://i.ytimg.com/vi/0LXopQsi8Cc/maxresdefault.jpg"
        }
    ],
 },
 {
    "tutorialCategory": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
    "tutorials": [
        { 
          "description": "(english) IGNOAPS",
          "videoLink": "https://youtu.be/qQi7hQOibDU?si=v7jvFSeObWnQrRZP",
          "uploadedBy": "Pension Info Channel",
          "uploadedDate": "2023-04-15",
          "thumbnail": "https://i.ytimg.com/vi/qQi7hQOibDU/maxresdefault.jpg"
        },
        {
            "description": "(hindi) IGNOAPS",
            "videoLink": "https://youtu.be/PEKj_ZtV_eg?si=qD9MHxKXk5UyeOAc",
          "uploadedBy": "Pension Yojana Hindi",
          "uploadedDate": "2023-05-01",
          "thumbnail": "https://th.bing.com/th?&id=OVP.q1Gfx2RWiLyuHS14BVMadAHgFo&w=321&h=180&c=7&pid=2.1&rs=1"
        },
        {
            "description": "(telugu) IGNOAPS",
            "videoLink": "https://youtu.be/7gN_pteb7x4?si=N7Y25SDgmpqFRWGK",
          "uploadedBy": "Pension Telugu Guide",
          "uploadedDate": "2023-05-15",
          "thumbnail": "https://i.ytimg.com/vi/7gN_pteb7x4/maxresdefault.jpg"
        }
        
    ]
 }
];
// Helper function to extract YouTube video ID from URL
const getYoutubeVideoId = (url) => {
  if (!url) return null;
  
  // Handle youtu.be format
  if (url.includes('youtu.be')) {
    const id = url.split('youtu.be/')[1]?.split('?')[0];
    return id || null;
  }
  
  // Handle youtube.com format
  const regExp = /^.(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : null;
};

// Component to render a single tutorial card
const TutorialCard = ({ tutorial, onSelect }) => {
  return (
    <div 
      className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer transition hover:scale-105"
      onClick={() => onSelect(tutorial)}
    >
      <div className="relative">
        <img 
          src={tutorial.thumbnail || "/api/placeholder/320/180"} 
          alt={tutorial.description}
          className="w-full h-40 object-cover"
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = "/api/placeholder/320/180";
          }}
        />
      </div>
      <div className="p-4">
        <h3 className="text-lg font-medium text-gray-900">{tutorial.description}</h3>
        <p className="text-sm text-gray-500 mt-1">Uploaded: {tutorial.uploadedDate}</p>
      </div>
    </div>
  );
};

// Component to render YouTube embed
const YouTubeEmbed = ({ videoId }) => {
  if (!videoId) return null;
  
  return (
    <div className="w-full">
      <iframe
        className="w-full h-96 rounded-lg"
      src={`https://www.youtube.com/embed/${videoId}`}
  title="YouTube video player"
        frameBorder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      ></iframe>
    </div>
  );
};

// Filter tutorials by language
const filterByLanguage = (tutorials, language) => {
  if (!language || language === 'all') return tutorials;
  
  return tutorials.filter(tutorial => 
    tutorial.description.toLowerCase().includes(language.toLowerCase())
  );
};

// Main TutorialViewer component
export default function TutorialViewer() {
  // Initialize with first category if available
  const [selectedCategory, setSelectedCategory] = useState(tutorialData[0]?.tutorialCategory || '');
  const [selectedLanguage, setSelectedLanguage] = useState('all');
  const [selectedTutorial, setSelectedTutorial] = useState(null);
  
  // Get tutorials for selected category
  const categoryTutorials = tutorialData.find(
    category => category.tutorialCategory === selectedCategory
  )?.tutorials || [];
  
  // Filter tutorials by language
  const filteredTutorials = filterByLanguage(categoryTutorials, selectedLanguage);
  
  // Reset selected tutorial when changing category or language
  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    setSelectedTutorial(null);
  };
  
  const handleLanguageChange = (language) => {
    setSelectedLanguage(language);
    setSelectedTutorial(null);
  };
  
  // Get video ID for selected tutorial
  const selectedVideoId = selectedTutorial ? getYoutubeVideoId(selectedTutorial.videoLink) : null;
  
  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Tutorial Videos</h1>
        
        {/* Category Navigation */}
        <div className="mb-6 overflow-x-auto">
          <div className="flex space-x-2 pb-2">
            {tutorialData.map((category) => (
              <button
                key={category.tutorialCategory}
                className={`px-4 py-2 rounded-lg whitespace-nowrap ${
                  selectedCategory === category.tutorialCategory
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-200'
                }`}
                onClick={() => handleCategoryChange(category.tutorialCategory)}
              >
                {category.tutorialCategory}
              </button>
            ))}
          </div>
        </div>
        
        {/* Language Filter */}
        <div className="mb-6 flex justify-center">
          <div className="inline-flex bg-white rounded-lg p-1 shadow-md">
            <button
              className={`px-4 py-2 rounded-lg ${
                selectedLanguage === 'all' ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-200'
              }`}
              onClick={() => handleLanguageChange('all')}
            >
              All
            </button>
            <button
              className={`px-4 py-2 rounded-lg ${
                selectedLanguage === 'hindi' ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-200'
              }`}
              onClick={() => handleLanguageChange('hindi')}
            >
              Hindi
            </button>
            <button
              className={`px-4 py-2 rounded-lg ${
                selectedLanguage === 'telugu' ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-200'
              }`}
              onClick={() => handleLanguageChange('telugu')}
            >
              Telugu
            </button>
            <button
              className={`px-4 py-2 rounded-lg ${
                selectedLanguage === 'english' ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-200'
              }`}
              onClick={() => handleLanguageChange('english')}
            >
              English
            </button>
          </div>
        </div>
        
        {/* Selected Video */}
        {selectedTutorial && (
          <div className="mb-8">
            <div className="bg-white p-4 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-4">{selectedTutorial.description}</h2>
              <YouTubeEmbed videoId={selectedVideoId} />
              <div className="mt-4 flex justify-between items-center">
                <button
                  className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors text-gray-700"
                  onClick={() => setSelectedTutorial(null)}
                >
                  Back to tutorials
                </button>
                <a
                  href={selectedTutorial.videoLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  Open on YouTube
                </a>
              </div>
            </div>
          </div>
        )}
        
        {/* Tutorial Grid */}
        {!selectedTutorial && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {filteredTutorials.length > 0 ? (
              filteredTutorials.map((tutorial, index) => (
                <TutorialCard
                  key={index}
                  tutorial={tutorial}
                  onSelect={setSelectedTutorial}
                />
              ))
            ) : (
              <div className="col-span-full text-center py-12 text-gray-500">
                No tutorials found for the selected filters.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}