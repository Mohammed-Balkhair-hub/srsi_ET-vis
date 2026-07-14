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
  ],
};
