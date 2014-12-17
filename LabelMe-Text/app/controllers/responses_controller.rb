class ResponsesController < ApplicationController
  before_action :signed_in_user

  def new
    @response = Response.new
    @post,@sentence = current_user.get_post_and_sentence
    if @post == nil
      if current_user.current_upload == nil
        flash[:error] = "Please choose a project to label"
        redirect_to edit_user_path(current_user, :form => "project"), 'data-no-turbolink' => true
        return
      end
      flash[:error] = "No more posts to label"
      redirect_to current_user
    else
    @fields = @post.label_fields
    @bold = @post.upload.sentences ? @post.highlight_sentence(@sentence.content) : @sentence.content
    end
  end

  def show
  end

  def create
    @post = current_user.get_post
    params[:response][:label] = apply_label_boxes
    @response = current_user.responses.build(response_params)
    if @response.save
      flash[:success] = "Response saved"
      current_user.set_current_post_to_next_sentence
    end
    redirect_to label_path
  end

  private
    def apply_label_boxes
      new_label = []
      for param in params.keys
        for category in @post.upload.label_categories
          for tag in category.label_tags
            if tag.content.include?(param)
              new_label.push(category.content + "@" + param.to_str)
            end
          end
        end
      end
      return new_label
    end

    def signed_in_user
      redirect_to(root_path) unless current_user != nil
    end    

    def response_params
      params.require(:response).permit(:sentence_id,:label => [])
    end
end
