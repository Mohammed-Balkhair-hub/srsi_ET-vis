window.SRSI = {
  program: "SRSI Emerging Technologies Track",
  org: "KAUST Academy",
  topics: [
    {
      id: "cnn",
      title: "Convolutional Neural Networks",
      blurb: "Kernels, padding, pooling, and the full forward pipeline — watch each section in order.",
      status: "available",
      href: "topics/cnn.html",
      zip: "downloads/cnn-videos.zip",
      videoDir: "videos/cnn",
      sections: [
        {
          id: "why",
          title: "1 · Why CNNs",
          blurb: "Why flat MLPs struggle with images, and how local filters + parameter sharing solve it.",
          file: "01_WhyCNNs.mp4",
        },
        {
          id: "conv",
          title: "2 · Convolution",
          blurb: "Multiply → products → sum: one kernel builds one feature map; stack many channels.",
          file: "02_ConvolutionMath.mp4",
        },
        {
          id: "pad",
          title: "3 · Padding & Stride",
          blurb: "Valid vs same padding, stride, and the output-size formula.",
          file: "03_PaddingAndStride.mp4",
        },
        {
          id: "pool",
          title: "4 · Pooling",
          blurb: "MaxPool and AvgPool window walkthroughs — downsample without learnable weights.",
          file: "04_Pooling.mp4",
        },
        {
          id: "pipe",
          title: "5 · CNN Pipeline",
          blurb: "Conv → BN → ReLU → Pool → Flatten → FC → Softmax, with shapes updating live.",
          file: "05_CNNPipeline.mp4",
        },
      ],
    },
    {
      id: "rnn",
      title: "Recurrent Neural Networks",
      blurb: "Why sequences need memory, one-step cell math, unrolling over time, and task shapes.",
      status: "available",
      href: "topics/rnn.html",
      zip: "downloads/rnn-videos.zip",
      videoDir: "videos/rnn",
      sections: [
        {
          id: "why",
          title: "1 · Why RNNs",
          blurb: "Order matters in sequences — keep a hidden state that depends on the past.",
          file: "01_WhyRNNs.mp4",
        },
        {
          id: "cell",
          title: "2 · One Timestep",
          blurb: "Products → sum → tanh: W_xh x_t and W_hh h_{t-1} with shared weights.",
          file: "02_RNNCellMath.mp4",
        },
        {
          id: "unroll",
          title: "3 · Unroll Over Time",
          blurb: "Same cell for t = 1…3 — watch memory carry forward when x_t is zero.",
          file: "03_UnrollSequence.mp4",
        },
        {
          id: "tasks",
          title: "4 · Tasks & Limits",
          blurb: "Many-to-one vs many-to-many, plus vanishing-gradient intuition.",
          file: "04_RNNTasks.mp4",
        },
      ],
    },
  ],
};
