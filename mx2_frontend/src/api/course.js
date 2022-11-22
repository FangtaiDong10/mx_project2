import axios from "../utils/http";

export const getCourse = async (courseId) => {
  const response = await axios.get("/courses/" + courseId);
  return response.data;
};

export const getCourseList = async () => {
  const response = await axios.get("/courses/");
  return response.data;
};

export const getLectureList = async (courseId) => {
  const response = await axios.get("/courses/" + courseId + "/lectures");
  return response.data;
};

export const uploadAttachment = async (
  courseId,
  lectureId,
  file,
  name,
  type,
  onUploadProgress
) => {
  const form = new FormData();
  form.append("file", file);
  form.append("metadata", JSON.stringify({ name, type }));

  const response = await axios.post(
    `/courses/${courseId}/lectures/${lectureId}/attachments`,
    form,
    {
      onUploadProgress,
    }
  );
  return response.data;
};

export const createLecture = async (
  courseId,
  title,
  streaming_url,
  recording_url,
  scheduled_time
) => {
  const response = await axios.post(`/courses/${courseId}/lectures`, {
    title,
    streaming_url,
    recording_url,
    scheduled_time,
  });
  return response.data;
};
