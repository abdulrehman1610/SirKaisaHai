<template>
  <div class="relative inline-flex items-center justify-center select-none w-full max-w-[300px] sm:max-w-[330px]">
    <svg
      viewBox="0 0 340 270"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      class="w-full h-auto"
      role="img"
      aria-label="Anonymous student ghost reading a book wearing a graduation cap"
    >
      <!-- Playful Ink Accent Sparks -->
      <path d="M58 108L43 97" stroke="#22151E" stroke-width="4" stroke-linecap="round" />
      <path d="M47 124L34 123" stroke="#22151E" stroke-width="4" stroke-linecap="round" />
      <path d="M244 65L255 54" stroke="#22151E" stroke-width="4" stroke-linecap="round" />
      <path d="M254 81L266 77" stroke="#22151E" stroke-width="4" stroke-linecap="round" />

      <!-- Ghost Body (Pale Lilac-Mist with Chunky Ink Outline) -->
      <path
        d="M112 162C112 104 126 66 168 66C209 66 226 104 226 162L228 190L110 190L112 162Z"
        fill="#CBC0D9"
        stroke="#22151E"
        stroke-width="5.5"
        stroke-linejoin="round"
      />
      <!-- Soft inner shading on ghost left curve -->
      <path
        d="M123 158C123 116 132 86 155 77"
        stroke="#DFD7EA"
        stroke-width="6"
        stroke-linecap="round"
        opacity="0.7"
      />

      <!-- Ghost Eyes -->
      <ellipse cx="152" cy="116" rx="8.5" ry="15" fill="#22151E" />
      <ellipse cx="182" cy="116" rx="8.5" ry="15" fill="#22151E" />

      <!-- Graduation Cap (Tilted playfully on top) -->
      <g transform="rotate(-9 165 65)">
        <!-- Cap base -->
        <path
          d="M128 57L128 73C128 80 144 85 166 85C188 85 204 80 204 73L204 57"
          fill="#352030"
          stroke="#22151E"
          stroke-width="5"
          stroke-linejoin="round"
        />
        <!-- Cap mortarboard diamond -->
        <polygon
          points="166,30 226,52 166,72 106,52"
          fill="#22151E"
          stroke="#22151E"
          stroke-width="4.5"
          stroke-linejoin="round"
        />
        <!-- Center button -->
        <circle cx="166" cy="51" r="4" fill="#E7DBE3" />
        <!-- Tassel cord hanging on left -->
        <path
          d="M164 52C143 56 122 62 117 77L115 95"
          stroke="#22151E"
          stroke-width="4.2"
          stroke-linecap="round"
        />
        <path
          d="M115 94L109 108M115 94L115 110M115 94L121 108"
          stroke="#22151E"
          stroke-width="3.6"
          stroke-linecap="round"
        />
      </g>

      <!-- Floating Chat Bubble (Right side, 3 dots) -->
      <g transform="translate(230, 96) rotate(4)">
        <path
          d="M14 4H74C82 4 88 10 88 18V46C88 54 82 60 74 60H32L14 72V60C6 60 0 54 0 46V18C0 10 6 4 14 4Z"
          fill="#CBC0D9"
          stroke="#22151E"
          stroke-width="5"
          stroke-linejoin="round"
        />
        <circle cx="28" cy="32" r="4.8" fill="#22151E" />
        <circle cx="46" cy="32" r="4.8" fill="#22151E" />
        <circle cx="64" cy="32" r="4.8" fill="#22151E" />
      </g>

      <!-- Open Book Cover (Dark Plum-Ink Base) -->
      <path
        d="M36 164L168 184L284 160L298 228L168 250L48 226L36 164Z"
        fill="#2B1926"
        stroke="#22151E"
        stroke-width="5.5"
        stroke-linejoin="round"
      />

      <!-- Open Book Pages (Warm Pearl White) -->
      <path
        d="M44 156C88 148 134 154 166 174C198 152 242 146 280 154L290 216C250 208 202 214 166 234C132 214 86 208 54 216L44 156Z"
        fill="#FAF7F9"
        stroke="#22151E"
        stroke-width="5"
        stroke-linejoin="round"
      />
      <!-- Book Spine Crease -->
      <path d="M166 174V234" stroke="#22151E" stroke-width="4.5" stroke-linecap="round" />

      <!-- Subtle Page Text Lines (Left Page) -->
      <path d="M74 176C98 173 124 176 144 184" stroke="#C5B6C3" stroke-width="3.5" stroke-linecap="round" />
      <path d="M78 192C102 190 124 192 144 199" stroke="#C5B6C3" stroke-width="3.5" stroke-linecap="round" />

      <!-- Ghost Hands Gripping Book Edges -->
      <path
        d="M36 178C26 176 24 162 34 156C44 150 62 154 64 166C66 178 50 182 36 178Z"
        fill="#CBC0D9"
        stroke="#22151E"
        stroke-width="5"
        stroke-linejoin="round"
      />
      <path
        d="M272 174C282 174 294 166 294 155C294 145 280 142 269 148C260 153 262 174 272 174Z"
        fill="#CBC0D9"
        stroke="#22151E"
        stroke-width="5"
        stroke-linejoin="round"
      />

      <!-- Bookmark Ribbon Hanging Left -->
      <path
        d="M148 164L158 170L154 188L147 182L141 187L148 164Z"
        fill="#61204C"
        stroke="#22151E"
        stroke-width="3.2"
        stroke-linejoin="round"
      />

      <!-- Tilted Cream Paper Ribbon: "Your identity stays yours." -->
      <g transform="rotate(-6 218 206)">
        <rect
          x="108"
          y="190"
          width="206"
          height="36"
          rx="10"
          fill="#FAF6F8"
          stroke="#E5D7E0"
          stroke-width="1.5"
        />
        <text
          x="211"
          y="214"
          text-anchor="middle"
          fill="#5C2D4D"
          font-family="'Instrument Serif', Georgia, serif"
          font-style="italic"
          font-size="19"
        >
          Your identity stays yours.
        </text>
      </g>
    </svg>
  </div>
</template>
